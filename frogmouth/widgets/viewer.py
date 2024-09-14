"""The markdown viewer itself."""

from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Callable
from webbrowser import open as open_url

from httpx import URL, AsyncClient, HTTPStatusError, RequestError
from markdown_it import MarkdownIt
from mdit_py_plugins import front_matter
from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.message import Message
from textual.reactive import var
from textual.widgets import Markdown
from typing_extensions import Final

from .. import __version__
from ..dialogs import ErrorDialog
from ..utility.advertising import APPLICATION_TITLE, USER_AGENT

PLACEHOLDER = f"""\
# {APPLICATION_TITLE} {__version__}

Welcome to {APPLICATION_TITLE}!
"""


class History:
    """Holds the browsing history for the viewer."""

    MAXIMUM_HISTORY_LENGTH: Final[int] = 256
    """The maximum number of items we'll keep in history."""

    def __init__(self, history: list[Path | URL] | None = None) -> None:
        """Initialise the history object."""
        self._history: deque[Path | URL] = deque(
            history or [], maxlen=self.MAXIMUM_HISTORY_LENGTH
        )
        """The list that holds the history of locations visited."""
        self._current: int = max(len(self._history) - 1, 0)
        """The current location."""

    @property
    def location(self) -> Path | URL | None:
        """The current location in the history."""
        try:
            return self._history[self._current]
        except IndexError:
            return None

    @property
    def current(self) -> int | None:
        """The current location in history, or None if there is no current location."""
        return None if self.location is None else self._current

    @property
    def locations(self) -> list[Path | URL]:
        """The locations in the history."""
        return list(self._history)

    def remember(self, location: Path | URL) -> None:
        """Remember a new location in the history.

        Args:
            location: The location to remember.
        """
        self._history.append(location)
        self._current = len(self._history) - 1

    def back(self) -> bool:
        """Go back in the history.

        Returns:
            `True` if the location changed, `False` if not.
        """
        if self._current:
            self._current -= 1
            return True
        return False

    def forward(self) -> bool:
        """Go forward in the history.

        Returns:
            `True` if the location changed, `False` if not.
        """
        if self._current < len(self._history) - 1:
            self._current += 1
            return True
        return False

    def __delitem__(self, index: int) -> None:
        del self._history[index]
        self._current = max(len(self._history) - 1, self._current)


class Viewer(VerticalScroll, can_focus=True, can_focus_children=True):
    """The markdown viewer class."""

    DEFAULT_CSS = """
    Viewer {
        width: 1fr;
        scrollbar-gutter: stable;
    }
    """

    BINDINGS = [
        Binding("w,k", "scroll_up", "", show=False),
        Binding("s,j", "scroll_down", "", show=False),
        Binding("space", "page_down", "", show=False),
        Binding("b", "page_up", "", show=False),
    ]
    """Bindings for the Markdown viewer widget."""

    history: var[History] = var(History)
    """The browsing history."""

    viewing_location: var[bool] = var(False)
    """Is an actual location being viewed?"""

    class ViewerMessage(Message):
        """Base class for viewer messages."""

        def __init__(self, viewer: Viewer) -> None:
            """Initialise the message.

            Args:
                viewer: The viewer sending the message.
            """
            super().__init__()
            self.viewer: Viewer = viewer
            """The viewer that sent the message."""

    class LocationChanged(ViewerMessage):
        """Message sent when the viewer location changes."""

    class HistoryUpdated(ViewerMessage):
        """Message sent when the history is updated."""

    def compose(self) -> ComposeResult:
        """Compose the markdown viewer."""
        yield Markdown(
            PLACEHOLDER,
            parser_factory=lambda: MarkdownIt("gfm-like").use(
                front_matter.front_matter_plugin
            ),
        )

    @property
    def document(self) -> Markdown:
        """The markdown document."""
        return self.query_one(Markdown)

    @property
    def location(self) -> Path | URL | None:
        """The location that is currently being visited."""
        return self.history.location if self.viewing_location else None

    def scroll_to_block(self, block_id: str) -> None:
        """Scroll the document to the given block ID.

        Args:
            block_id: The ID of the block to scroll to.
        """
        self.scroll_to_widget(self.document.query_one(f"#{block_id}"), top=True)

    def _post_load(self, location: Path | URL, remember: bool = True) -> None:
        """Perform some post-load tasks.

        Args:
            location: The location that has been loaded.
            remember: Should we remember the location in the history?
        """
        # We've loaded something fresh, ensure we're at the top.
        self.scroll_home(animate=False)
        # If we've made it in here we are viewing an actual location.
        self.viewing_location = True
        # Remember the location in the history if we're supposed to.
        if remember:
            self.history.remember(location)
            self.post_message(self.HistoryUpdated(self))
        # Let anyone else know we've changed location.
        self.post_message(self.LocationChanged(self))

    @work(exclusive=True)
    async def _local_load(self, location: Path, remember: bool = True) -> None:
        """Load a Markdown document from a local file.

        Args:
            location: The location to load from.
            remember: Should we remember the location in th ehistory?
        """
        try:
            await self.document.load(location)
        except OSError as error:
            self.app.push_screen(
                ErrorDialog(
                    "Error loading local document",
                    f"{location}\n\n{error}.",
                )
            )
        else:
            self._post_load(location, remember)

    @work(exclusive=True)
    async def _remote_load(self, location: URL, remember: bool = True) -> None:
        """Load a Markdown document from a URL.

        Args:
            location: The location to load from.
            remember: Should we remember the location in the history?
        """

        try:
            async with AsyncClient() as client:
                response = await client.get(
                    location,
                    follow_redirects=True,
                    headers={"user-agent": USER_AGENT},
                )
        except RequestError as error:
            self.app.push_screen(ErrorDialog("Error getting document", str(error)))
            return

        try:
            response.raise_for_status()
        except HTTPStatusError as error:
            self.app.push_screen(ErrorDialog("Error getting document", str(error)))
            return

        # There didn't seem to be an error transporting the data, and
        # neither did there seem to be an error with the resource itself. So
        # at this point we should hopefully have the document's content.
        # However... it's possible we've been fooled into loading up
        # something that looked like it was a markdown file, but really it's
        # a web-rendering of such a file; so as a final check we make sure
        # we're looking at something that's plain text, or actually
        # Markdown.
        content_type = response.headers.get("content-type", "")
        if any(
            content_type.startswith(f"text/{sub_type}")
            for sub_type in ("plain", "markdown", "x-markdown")
        ):
            self.document.update(response.text)
            self._post_load(location, remember)
        else:
            # Didn't look like something we could handle with the Markdown
            # viewer. We could throw up an error, or we could just be nice
            # to the user. Let's be nice...
            open_url(str(location))

    def visit(self, location: Path | URL, remember: bool = True, focus:bool=True) -> None:
        """Visit a location.

        Args:
            location: The location to visit.
            remember: Should this visit be added to the history?
        """
        # Based on the type of the location, load up the content.
        if isinstance(location, Path):
            self.can_focus = focus
            self._local_load(location.expanduser().resolve(), remember)
        elif isinstance(location, URL):
            self._remote_load(location, remember)
        else:
            raise ValueError("Unknown location type passed to the Markdown viewer")

    def reload(self) -> None:
        """Reload the current location."""
        if self.location is not None:
            self.visit(self.location, False)

    def show(self, content: str) -> None:
        """Show some direct text in the viewer.

        Args:
            content: The text to show.
        """
        self.viewing_location = False
        self.document.update(content)
        self.scroll_home(animate=False)

    def _jump(self, direction: Callable[[], bool]) -> None:
        """Jump in a particular direction within the history.

        Args:
            direction: A function that jumps in the desired direction.
        """
        if direction():
            if self.history.location is not None:
                self.visit(self.history.location, remember=False)

    def back(self) -> None:
        """Go back in the viewer history."""
        self._jump(self.history.back)

    def forward(self) -> None:
        """Go forward in the viewer history."""
        self._jump(self.history.forward)

    def load_history(self, history: list[Path | URL]) -> None:
        """Load up a history list from the given history.

        Args:
            history: The history load up from.
        """
        self.history = History(history)
        self.post_message(self.HistoryUpdated(self))

    def delete_history(self, history_id: int) -> None:
        """Delete an item from the history.

        Args:
            history_id: The ID of the history item to delete.
        """
        try:
            del self.history[history_id]
        except IndexError:
            pass
        else:
            self.post_message(self.HistoryUpdated(self))

    def clear_history(self) -> None:
        """Clear down the whole of history."""
        self.load_history([])
