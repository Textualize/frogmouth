"""The main screen for the application."""

from __future__ import annotations

from pathlib import Path

from httpx import AsyncClient, Response

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.events import Paste
from textual.screen import Screen
from textual.widgets import Footer, Header

from .. import __version__
from ..widgets import Navigation, Omnibox, Viewer

PLACEHOLDER = """\
# Textual Markdown Viewer

Welcome to the Textual Markdown viewer!
"""


class Main(Screen):
    """The main screen for the application."""

    DEFAULT_CSS = """
    Viewer {
        width: 3fr;
    }

    MarkdownTableOfContents {
        max-width: 25%;
    }
    """

    BINDINGS = [
        Binding("escape", "escape", "Escpae", show=False),
        Binding("/", "omnibox", "Omnibox", show=False),
        Binding("ctrl+b", "bookmarks", "Bookmarks"),
        Binding("ctrl+l", "local_files", "Local Files"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the main screen.."""
        yield Header()
        yield Omnibox()
        with Horizontal():
            yield Navigation()
            yield Viewer(PLACEHOLDER, show_table_of_contents=False)
        yield Footer()

    async def visit(self, location: Path | Response) -> None:
        """Visit the given location.

        Args:
            location: The location to visit.
        """
        self.query_one(Viewer).focus()
        if isinstance(location, Path):
            self.query_one(Omnibox).visiting = str(location)
            await self.query_one(Viewer).go(location)
        else:
            # TODO: This is a bit of a hack right at the moment; really I
            # want the URL to be coming in here and things flowing from
            # there. But right now I just want to get the text showing.
            self.query_one(Omnibox).visiting = str(location.url)
            self.query_one(Viewer).document.update(location.text)

    def on_mount(self) -> None:
        """Set up the main screen once the DOM is ready."""
        self.query_one(Omnibox).focus()

    async def on_omnibox_local_view_command(
        self, event: Omnibox.LocalViewCommand
    ) -> None:
        """Handle the omnibox asking us to view a particular file."""
        await self.visit(event.path)

    async def on_omnibox_remote_view_command(
        self, event: Omnibox.RemoteViewCommand
    ) -> None:
        """Handle the omnibox asking us to view a particular URL.

        Args:
            event: The remote view event.
        """
        async with AsyncClient() as client:
            response = await client.get(
                event.url,
                follow_redirects=True,
                headers={"user-agent": f"textual-markdown-client v{__version__}"},
            )
            # TODO: Lots of error handling.
            await self.visit(response)

    def on_omnibox_quit_command(self) -> None:
        """Handle being asked to quit."""
        self.app.exit()

    async def on_navigation_visit_local_file(
        self, event: Navigation.VisitLocalFile
    ) -> None:
        """Visit a local file in the viewer.

        Args:
            event: The event to handle.
        """
        await self.visit(event.visit)

    async def on_paste(self, event: Paste) -> None:
        """Handle a paste event.

        Args:
            event: The paste event.

        This method is here to capture paste events that look like the name
        of a local file (later I may add URL support too).
        """
        if (candidate_file := Path(event.text)).exists():
            await self.visit(candidate_file)

    def action_escape(self) -> None:
        """Process the escape key."""
        if self.query_one(Omnibox).has_focus:
            self.app.exit()
        else:
            self.query_one(Omnibox).focus()

    def action_omnibox(self) -> None:
        """Jump to the omnibox."""
        self.query_one(Omnibox).focus()

    def action_local_files(self) -> None:
        """Display and focus the local files selection pane."""
        self.query_one(Navigation).jump_to_local_files()

    def action_bookmarks(self) -> None:
        """Display and focus the bookmarks selection pane."""
        self.query_one(Navigation).jump_to_bookmarks()
