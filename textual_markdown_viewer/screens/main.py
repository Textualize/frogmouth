"""The main screen for the application."""

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Footer, Header, MarkdownViewer


from ..widgets import Navigation, Omnibox


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
            yield MarkdownViewer(
                "# TODO\n\n- [ ] Pretty much everything.\n- [ ] And then some."
            )
        yield Footer()

    def on_mount(self) -> None:
        """Set up the main screen once the DOM is ready."""
        self.query_one(Omnibox).focus()

    def on_omnibox_quit_command(self) -> None:
        """Handle being asked to quit."""
        self.app.exit()
