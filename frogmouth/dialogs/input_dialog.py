"""Provides a modal dialog for getting a value from the user."""

from __future__ import annotations

from typing import NamedTuple

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Button, Input, Label


class InputDialogResult(NamedTuple):
    """The result of input with an `InputDialog`."""

    dialog_id: str | None
    """The ID of the dialog returning the result."""

    value: str
    """The input value."""


class InputDialog(ModalScreen[InputDialogResult]):
    """A modal dialog for getting a single input from the user."""

    DEFAULT_CSS = """
    InputDialog {
        align: center middle;
    }

    InputDialog > Vertical {
        background: $panel;
        height: auto;
        width: auto;
        border: thick $primary;
    }

    InputDialog > Vertical > * {
        width: auto;
        height: auto;
    }

    InputDialog Input {
        width: 40;
        margin: 1;
    }

    InputDialog Label {
        margin-left: 2;
    }

    InputDialog Button {
        margin-right: 1;
    }

    InputDialog #buttons {
        width: 100%;
        align-horizontal: right;
        padding-right: 1;
    }
    """
    """The default styling for the input dialog."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "", show=False),
    ]
    """Bindings for the dialog."""

    def __init__(  # pylint:disable=redefined-builtin
        self,
        requester: Widget,
        prompt: str,
        initial: str | None = None,
        id: str | None = None,
    ) -> None:
        """Initialise the input dialog.

        Args:
            requester: The widget requesting the input.
            prompt: The prompt for the input.
            initial: The initial value for the input.
            cargo: Any cargo value for the input.
            id: The ID for the dialog.
        """
        super().__init__(id=id)
        self._requester = requester
        """A reference to the widget requesting the input."""
        self._prompt = prompt
        """The prompt to display for the input."""
        self._initial = initial
        """The initial value to use for the input."""

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        with Vertical():
            with Vertical(id="input"):
                yield Label(self._prompt)
                yield Input(self._initial or "")
            with Horizontal(id="buttons"):
                yield Button("OK", id="ok", variant="primary")
                yield Button("Cancel", id="cancel")

    def on_mount(self) -> None:
        """Set up the dialog once the DOM is ready."""
        self.query_one(Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle one of the dialog's buttons been pressed.

        Args:
            event: The button press event.
        """
        if event.button.id == "cancel":
            self.app.pop_screen()
        elif event.button.id == "ok" and self.query_one(Input).value.strip():
            self.dismiss(InputDialogResult(self.id, self.query_one(Input).value))

    def on_input_submitted(self) -> None:
        """Do default processing when the user hits enter in the input."""
        self.query_one("#ok", Button).press()
