"""Provides the Markdown viewer's omnibox widget."""

from textual.message import Message
from textual.widgets import Input


class Omnibox(Input):
    """The command and location input widget for the Markdown viewer."""

    DEFAULT_CSS = """
    Omnibox {
        border-left: none;
        border-right: none;
    }

    Omnibox:focus {
        border-left: none;
        border-right: none;
    }
    """

    class QuitCommand(Message):
        """The quit command."""

    @staticmethod
    def _command_like(value: str) -> bool:
        """Does the given string look command-like?

        Args:
            value: The value to check for command-likeness.

        Returns:
            `True` if the value looks like a command, `False` if not.
        """
        return len(value.split()) == 1

    def _is_command(self, value: str) -> bool:
        """Is the given string a known command?

        Args:
            value: The value to check.

        Returns:
            `True` if the string is a known command, `False` if not.
        """
        return (
            self._command_like(value)
            and getattr(self, f"command_{value}", None) is not None
        )

    def _execute_command(self, command: str) -> None:
        """Execute the given command.

        Args:
            command: The comment to execute.
        """
        getattr(self, f"command_{command}")()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle the user submitting the input.

        Args:
            event: The submit event.
        """
        cleaned = self.value.strip().lower()
        if self._is_command(cleaned):
            event.stop()
            self._execute_command(cleaned)

    def command_quit(self) -> None:
        """The quit command."""
        self.post_message(self.QuitCommand())
