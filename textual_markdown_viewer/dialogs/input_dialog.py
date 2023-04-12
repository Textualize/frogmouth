"""Provides a modal dialog for getting a value from the user."""

from __future__ import annotations

from typing import Any

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label
from textual.widget import Widget


class InputDialog(ModalScreen):
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
        align-horizontal: right !important;
        padding-right: 1;
    }
    """
    """The default styling for the input dialog."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "", show=False),
    ]
    """Bindings for the dialog."""

    def __init__(  # pylint:disable=redefined-builtin,too-many-arguments
        self,
        requester: Widget,
        prompt: str,
        initial: str | None = None,
        cargo: Any = None,
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
        self._cargo = cargo
        """Any cargo data for the input dialog."""

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

    class Result(Message):
        """The input dialog result message."""

        def __init__(
            self, sender_id: str | None, value: str, cargo: Any = None
        ) -> None:
            """Initialise the result message.

            Args:
                input_dialog: The input dialog sending the message.
                value: The value to attach as the result.
                cargo: Any cargo data for the result.
            """
            super().__init__()
            self.sender_id = sender_id
            """The ID of the sending dialog."""
            self.value: str = value
            """The value of the result."""
            self.cargo: Any = cargo
            """Cargo data for the result."""

    def _return_input(self) -> None:
        """Return the input value from the dialog."""
        self._requester.post_message(
            self.Result(self.id, self.query_one(Input).value, self._cargo)
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle one of the dialog's buttons been pressed.

        Args:
            event: The button press event.
        """
        if event.button.id == "cancel":
            self.app.pop_screen()
        elif event.button.id == "ok" and self.query_one(Input).value.strip():
            self._return_input()
            self.app.pop_screen()
