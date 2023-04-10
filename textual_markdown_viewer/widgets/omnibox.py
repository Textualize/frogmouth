"""Provides the Markdown viewer's omnibox widget."""

from __future__ import annotations

from pathlib import Path

from httpx import URL
from textual.message import Message
from textual.reactive import var
from textual.widgets import Input

from ..utility import is_likely_url


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

    Omnibox .input--placeholder {
        color: $text 70%;
        text-style: italic;
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

    visiting: var[str] = var("")
    """The location that is being visited."""

    def watch_visiting(self) -> None:
        """Watch the visiting reactive variable."""
        self.placeholder = self.visiting or "Enter a location or command"
        if self.visiting:
            self.value = self.visiting

    _ALIASES: dict[str, str] = {
        "a": "about",
        "c": "contents",
        "cd": "chdir",
        "h": "history",
        "l": "local",
        "toc": "contents",
        "q": "quit",
    }
    """Command aliases."""

    @staticmethod
    def _split_command(value: str) -> list[str]:
        """Split a value into a command and argument tail.

        Args:
            value: The value to split.

        Returns:
            A list of the command and the argument(s).
        """
        command = value.split(None, 1)
        return [*command, ""] if len(command) == 1 else command

    def _is_command(self, value: str) -> bool:
        """Is the given string a known command?

        Args:
            value: The value to check.

        Returns:
            `True` if the string is a known command, `False` if not.
        """
        command, *_ = self._split_command(value)
        return (
            getattr(self, f"command_{self._ALIASES.get(command, command)}", None)
            is not None
        )

    def _execute_command(self, command: str) -> None:
        """Execute the given command.

        Args:
            command: The comment to execute.
        """
        command, arguments = self._split_command(command)
        getattr(self, f"command_{self._ALIASES.get(command, command)}")(
            arguments.strip()
        )

    class LocalChdirCommand(Message):
        """Command for changing the local files directory."""

        def __init__(self, target: Path) -> None:
            """Initialise the local files chdir command."""
            super().__init__()
            self.target = target
            """The target directory to change to."""

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle the user submitting the input.

        Args:
            event: The submit event.
        """
        submitted = self.value.strip()
        if is_likely_url(submitted):
            self.post_message(self.RemoteViewCommand(URL(submitted)))
        elif (path := Path(submitted)).exists():
            if path.is_file():
                self.post_message(self.LocalViewCommand(path))
            elif path.is_dir():
                self.post_message(self.LocalChdirCommand(path))
            else:
                return
        elif self._is_command(command := submitted.lower()):
            self._execute_command(command)
        else:
            return
        self.value = ""
        event.stop()

    class ContentsCommand(Message):
        """The table of contents command."""

    def command_contents(self, _: str) -> None:
        """Handle the table of contents command."""
        self.post_message(self.ContentsCommand())

    class LocalFilesCommand(Message):
        """The local files command."""

    def command_local(self, _: str) -> None:
        """View the local files."""
        self.post_message(self.LocalFilesCommand())

    class QuitCommand(Message):
        """The quit command."""

    def command_quit(self, _: str) -> None:
        """The quit command."""
        self.post_message(self.QuitCommand())

    class HistoryCommand(Message):
        """The history command."""

    def command_history(self, _: str) -> None:
        """The history command."""
        self.post_message(self.HistoryCommand())

    class AboutCommand(Message):
        """The about command."""

    def command_about(self, _: str) -> None:
        """The about command."""
        self.post_message(self.AboutCommand())

    def command_chdir(self, target: str) -> None:
        """The chdir command."""
        self.post_message(self.LocalChdirCommand(Path(target)))
