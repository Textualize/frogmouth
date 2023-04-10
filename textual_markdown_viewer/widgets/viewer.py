"""The markdown viewer itself."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from httpx import AsyncClient, URL, HTTPStatusError, RequestError

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.message import Message
from textual.reactive import var
from textual.widgets import Markdown

from .. import __version__
from ..screens.dialog import ErrorDialog

PLACEHOLDER = f"""\
# Textual Markdown Viewer {__version__}

Welcome to the Textual Markdown viewer!
"""


class History:
    """Holds the browsing history for the viewer."""

    def __init__(self) -> None:
        """Initialise the history object."""
        self._history: list[Path | URL] = []
        """The list that holds the history of locations visited."""
        self._current: int = 0
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
        return self._history

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


class Viewer(VerticalScroll, can_focus=True, can_focus_children=True):
    """The Markdown viewer class."""

    DEFAULT_CSS = """
    Viewer {
        width: 3fr;
    }
    """

    history: var[History] = var(History)
    """The browsing history."""

    class LocationChanged(Message):
        """Message sent when the viewer location changes."""

        def __init__(self, viewer: Viewer) -> None:
            """Initialise the location changed message.

            Args:
                viewer: The viewer sending the message.
            """
            super().__init__()
            self.viewer: Viewer = viewer
            """The viewer that sent the message."""

    class AddedToHistory(Message):
        """Message sent when something is added to history."""

        def __init__(self, location: Path | URL) -> None:
            """Initialise the location history recording message.

            Args:
                location: The location that was added to history.
            """
            super().__init__()
            self.location = location
            """The location added to history."""

    def compose(self) -> ComposeResult:
        """Compose the markdown viewer."""
        yield Markdown(PLACEHOLDER)

    @property
    def document(self) -> Markdown:
        """The markdown document."""
        return self.query_one(Markdown)

    @property
    def location(self) -> Path | URL | None:
        """The location that is currently being visited."""
        return self.history.location

    def scroll_to_block(self, block_id: str) -> None:
        """Scroll the document to the given block ID.

        Args:
            block_id: The ID of the block to scroll to.
        """
        self.scroll_to_widget(self.document.query_one(f"#{block_id}"), top=True)

    async def _local_load(self, location: Path) -> bool:
        """Load a Markdown document from a local file.

        Args:
            location: The location to load from.

        Returns:
            `True` if the document seemed to load fine, `False` if not.
        """
        # At the moment Textual's Markdown widget's load method captures
        # *all* exceptions and just returns a true/false. It would be
        # better to get an exception here and be able to properly report
        # the problem. Alas, right now, we can't.
        if not await self.document.load(location):
            self.app.push_screen(
                ErrorDialog(
                    "Error loading local document",
                    f"{location}\n\nThere was an error loading the document.",
                )
            )
            return False
        return True

    async def _remote_load(self, location: URL) -> bool:
        """Load a Markdown document from a URL.

        Args:
            location: The location to load from.

        Returns:
            `True` if the document seemed to load fine, `False` if not.
        """

        try:
            async with AsyncClient() as client:
                response = await client.get(
                    location,
                    follow_redirects=True,
                    headers={"user-agent": f"textual-markdown-client v{__version__}"},
                )
        except RequestError as error:
            self.app.push_screen(ErrorDialog("Error getting document", str(error)))
            return False

        try:
            response.raise_for_status()
        except HTTPStatusError as error:
            self.app.push_screen(ErrorDialog("Error getting document", str(error)))
            return False

        # There didn't seem to be an error transporting the data, and
        # neither did there seem to be an error with the resource itself. So
        # at this point we should hopefully have the document's content.
        self.document.update(response.text)
        return True

    async def visit(self, location: Path | URL, remember: bool = True) -> None:
        """Visit a location.

        Args:
            location: The location to visit.
            remember: Should this visit be added to the history?
        """

        # Based on the type of the location, load up the content.
        loaded = False
        if isinstance(location, Path):
            loaded = await self._local_load(location)
        elif isinstance(location, URL):
            loaded = await self._remote_load(location)
        else:
            raise ValueError("Unknown location type passed to the Markdown viewer")

        # If we didn't manage to load anything don't do anything else for
        # the visit.
        if not loaded:
            return

        # Remember the location in the history if we're supposed to.
        if remember:
            self.history.remember(location)
            self.post_message(self.AddedToHistory(location))

        # Let anyone else know we've changed location.
        self.post_message(self.LocationChanged(self))

    async def _jump(self, direction: Callable[[], bool]) -> None:
        """Jump in a particular direction within the history.

        Args:
            direction: A function that jumps in the desired direction.
        """
        if direction():
            if self.history.location is not None:
                await self.visit(self.history.location, remember=False)

    async def back(self) -> None:
        """Go back in the viewer history."""
        await self._jump(self.history.back)

    async def forward(self) -> None:
        """Go forward in the viewer history."""
        await self._jump(self.history.forward)
