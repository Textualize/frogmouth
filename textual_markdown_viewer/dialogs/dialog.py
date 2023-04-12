"""Provides modal dialog screens for the application."""

from rich.text import TextType
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Static
from textual.widgets._button import ButtonVariant


class ModalDialog(ModalScreen):
    """Base modal dialog screen."""

    DEFAULT_CSS = """
    ModalDialog {
        align: center middle;
    }

    ModalDialog Center {
        width: 100%;
    }

    ModalDialog > Vertical {
        background: $panel;
        min-width: 30%;
        width: auto;
        height: auto;
        border: round $primary;
    }

    ModalDialog Static {
        width: auto;
    }

    ModalDialog .spaced {
        padding: 1;
    }

    ModalDialog #message {
        border-top: solid $primary;
        border-bottom: solid $primary;
    }
    """
    """Default CSS for the base modal dialog screen."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "", show=False),
    ]
    """Bindings for the base modal dialog screen."""

    def __init__(self, title: TextType, message: TextType) -> None:
        """Initialise the modal dialog.

        Args:
            title: The title for the dialog.
            message: The message to show.
        """
        super().__init__()
        self._title = title
        self._message = message

    @property
    def button_style(self) -> ButtonVariant:
        """The style for the dialog's button."""
        return "primary"

    def compose(self) -> ComposeResult:
        """Compose the content of the modal dialog."""
        with Vertical():
            with Center():
                yield Static(self._title, classes="spaced")
            yield Static(self._message, id="message", classes="spaced")
            with Center(classes="spaced"):
                yield Button("OK", variant=self.button_style)

    def on_mount(self) -> None:
        """Configure the dialog once the DOM has loaded."""
        self.query_one(Button).focus()

    def on_button_pressed(self) -> None:
        """Handle the OK button being pressed."""
        self.app.pop_screen()
