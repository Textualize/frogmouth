"""The main application class for the Markdown viewer."""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from .. import __version__


class MarkdownViewer(App[None]):
    """The main application class."""

    TITLE = "Textual Markdown Viewer"
    """The main title for the application."""

    SUB_TITLE = f"{__version__}"
    """The sub-title for the application."""

    def compose(self) -> ComposeResult:
        """Compose the child widgets.

        Returns:
            The widgets that compose the main application display.
        """
        yield Header()
        yield Footer()
