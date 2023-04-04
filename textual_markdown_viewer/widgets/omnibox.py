"""Provides the Markdown viewer's omnibox widget."""

from __future__ import annotations

from pathlib import Path

from httpx import URL

from textual.message import Message
from textual.reactive import var
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

    class LocalViewCommand(Message):
        """The local file view command."""

        def __init__(self, path: Path) -> None:
            """Initialise the local view command.

            Args:
                path: The path to view.
            """
            super().__init__()
            self.path = path
            """The path of the file to view."""

    class RemoteViewCommand(Message):
        """The remote file view command."""

        def __init__(self, url: URL) -> None:
            """Initialise the remove view command.

            Args:
                url: The URL of the remote file to view.
            """
            super().__init__()
            self.url = url
            """The URL of the file to view."""

    class QuitCommand(Message):
        """The quit command."""

    visiting: var[str] = var("")
    """The location that is being visited."""

    def watch_visiting(self) -> None:
        """Watch the visiting reactive variable."""
        self.placeholder = self.visiting or "Enter a location or command"

    @staticmethod
    def _command_like(value: str) -> bool:
        """Does the given string look command-like?

        Args:
            value: The value to check for command-likeness.

        Returns:
            `True` if the value looks like a command, `False` if not.
        """
        return len(value.split()) == 1

    _ALIASES: dict[str, str] = {"q": "quit"}
    """Command aliases."""

    def _is_command(self, value: str) -> bool:
        """Is the given string a known command?

        Args:
            value: The value to check.

        Returns:
            `True` if the string is a known command, `False` if not.
        """
        value = self._ALIASES.get(value, value)
        return (
            self._command_like(value)
            and getattr(self, f"command_{value}", None) is not None
        )

    @staticmethod
    def _is_likely_url(candidate: str) -> bool:
        """Does the given value look something like a URL?"""
        # Quick and dirty for now.
        url = URL(candidate)
        return url.is_absolute_url and url.scheme in ("http", "https")

    def _execute_command(self, command: str) -> None:
        """Execute the given command.

        Args:
            command: The comment to execute.
        """
        getattr(self, f"command_{self._ALIASES.get(command, command)}")()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle the user submitting the input.

        Args:
            event: The submit event.
        """
        cleaned = self.value.strip()
        lowered = cleaned.lower()
        if self._is_command(lowered):
            self._execute_command(lowered)
        elif Path(cleaned).exists():
            self.post_message(self.LocalViewCommand(Path(cleaned)))
        elif self._is_likely_url(cleaned):
            self.post_message(self.RemoteViewCommand(URL(cleaned)))
        else:
            return
        self.value = ""
        event.stop()

    def command_quit(self) -> None:
        """The quit command."""
        self.post_message(self.QuitCommand())
