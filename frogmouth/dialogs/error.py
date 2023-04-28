"""Provides an error dialog."""

from textual.widgets._button import ButtonVariant

from .text_dialog import TextDialog


class ErrorDialog(TextDialog):
    """Modal dialog for showing errors."""

    DEFAULT_CSS = """
    ErrorDialog > Vertical {
        background: $error 15%;
        border: thick $error 50%;
    }

    ErrorDialog #message {
        border-top: solid $panel;
        border-bottom: solid $panel;
    }
    """

    @property
    def button_style(self) -> ButtonVariant:
        """The style for the dialog's button."""
        return "error"
