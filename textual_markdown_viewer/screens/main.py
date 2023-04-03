"""The main screen for the application."""

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Footer, Header, MarkdownViewer


from ..widgets import Navigation, Omnibox

PLACEHOLDER = """\
# Textual Markdown Viewer

Welcome to the Textual Markdown viewer!
"""


class Main(Screen):
    """The main screen for the application."""

    DEFAULT_CSS = """
    MarkdownViewer {
        width: 4fr;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the main screen.."""
        yield Header()
        yield Omnibox(placeholder="Enter a location or command")
        with Horizontal():
            yield Navigation()
            yield MarkdownViewer(PLACEHOLDER)
        yield Footer()

    def on_mount(self) -> None:
        """Set up the main screen once the DOM is ready."""
        self.query_one(Omnibox).focus()

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
        await self.query_one(MarkdownViewer).go(event.visit)
