"""Provides the viewer's omnibox widget."""

from __future__ import annotations

from pathlib import Path
from re import compile as compile_regexp
from typing import Type
from webbrowser import open as open_url

from httpx import URL
from textual.message import Message
from textual.reactive import var
from textual.widgets import Input

from ..utility import is_likely_url
from ..utility.advertising import DISCORD, ORGANISATION_NAME, PACKAGE_NAME


class Omnibox(Input):
    """The command and location input widget for the viewer."""

    DEFAULT_CSS = """
    Omnibox {
        dock: top;
        padding: 0;
        height: 3;
    }

    Omnibox .input--placeholder {
        color: $text 50%;
    }
    """
    """Default styling for the omnibox."""

    visiting: var[str] = var("")
    """The location that is being visited."""

    def watch_visiting(self) -> None:
        """Watch the visiting reactive variable."""
        self.placeholder = self.visiting or "Enter a location or command"
        if self.visiting:
            self.value = self.visiting

    _ALIASES: dict[str, str] = {
        "a": "about",
        "b": "bookmarks",
        "bm": "bookmarks",
        "bb": "bitbucket",
        "c": "contents",
        "cb": "codeberg",
        "cd": "chdir",
        "cl": "changelog",
        "gh": "github",
        "gl": "gitlab",
        "h": "history",
        "l": "local",
        "obs": "obsidian",
        "toc": "contents",
        "q": "quit",
        "?": "help",
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

        # Clean up whatever the user input.
        submitted = self.value.strip()

        # Now that we've got it, empty the value. We'll put it back
        # depending on the outcome.
        self.value = ""

        # Work through the possible options for what the user entered.
        if is_likely_url(submitted):
            # It looks like it's an URL of some description so try and load
            # it as such.
            self.post_message(self.RemoteViewCommand(URL(submitted)))
        elif (path := Path(submitted).expanduser().resolve()).exists():
            # It's a match for something in the local filesystem. Is it...
            if path.is_file():
                # a file! Try and open it for viewing.
                self.post_message(self.LocalViewCommand(path))
                self.value = str(path)
            elif path.is_dir():
                # Nope, it's a directory. Take that to be a request to open
                # the local file selection navigation pane with the
                # directory as the root.
                self.post_message(self.LocalChdirCommand(path))
            else:
                # It's something that exists in the filesystem, but it's not
                # a directory or a file. Let's nope on that for now.
                return
        elif self._is_command(command := submitted.lower()):
            # Having checked for URLs and existing filesystem things, it's
            # now safe to look for commands. Having got here, it is a match
            # for a command so we handle it as such.
            self._execute_command(command)
        else:
            # Having got this far, the best thing to do now is assume that
            # the user was attempting to enter a filename to view and got it
            # wrong. So that they get some sort of feedback, let's attempt
            # to view it anyway.
            self.post_message(self.LocalViewCommand(Path(submitted)))
            # Because it'll raise an error and the user may want to edit the
            # input to get it right, we put the original input back in
            # place.
            self.value = submitted

        # If we got a match above stop the event.
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

    class BookmarksCommand(Message):
        """The bookmarks command."""

    def command_bookmarks(self, _: str) -> None:
        """View the bookmarks."""
        self.post_message(self.BookmarksCommand())

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

    class HelpCommand(Message):
        """The help command."""

    def command_help(self, _: str) -> None:
        """The help command."""
        self.post_message(self.HelpCommand())

    def command_chdir(self, target: str) -> None:
        """The chdir command.

        Args:
            target: The target directory to change to.
        """
        self.post_message(
            self.LocalChdirCommand(Path(target or "~").expanduser().resolve())
        )

    _GUESS_BRANCH = compile_regexp(
        r"^(?P<owner>[^/ ]+)[/ ](?P<repo>[^ :]+)(?: +(?P<file>[^ ]+))?$"
    )
    """Regular expression for matching a repo and file where we'll guess the branch."""

    _SPECIFIC_BRANCH = compile_regexp(
        r"^(?P<owner>[^/ ]+)[/ ](?P<repo>[^ :]+):(?P<branch>[^ ]+)(?: +(?P<file>[^ ]+))?$"
    )
    """Regular expression for matching a repo and file where the branch is also given."""

    class ForgeCommand(Message):
        """The base git forge quick load command."""

        def __init__(
            self,
            owner: str,
            repository: str,
            branch: str | None = None,
            desired_file: str | None = None,
        ) -> None:
            """Initialise the git forge quick load command."""
            super().__init__()
            self.owner = owner
            """The owner of the repository."""
            self.repository = repository
            """The repository."""
            self.branch: str | None = branch
            """The optional branch to attempt to pull the file from."""
            self.desired_file: str | None = desired_file
            """The optional file the user wants from the repository."""

    def _forge_quick_look(self, command: Type[ForgeCommand], tail: str) -> None:
        """Core forge quick look support method.

        Args:
            command: The command message to be posted.
            tail: The tail of the command to be parsed.
        """
        tail = tail.strip()
        if hit := self._GUESS_BRANCH.match(tail):
            self.post_message(
                command(hit["owner"], hit["repo"], desired_file=hit["file"])
            )
        elif hit := self._SPECIFIC_BRANCH.match(tail):
            self.post_message(
                command(
                    hit["owner"],
                    hit["repo"],
                    branch=hit["branch"],
                    desired_file=hit["file"],
                )
            )

    class GitHubCommand(ForgeCommand):
        """The GitHub quick load command."""

    def command_github(self, tail: str) -> None:
        """The github command.

        Args:
            tail: The tail of the command.
        """
        self._forge_quick_look(self.GitHubCommand, tail)

    class GitLabCommand(ForgeCommand):
        """The GitLab quick load command."""

    def command_gitlab(self, tail: str) -> None:
        """The Gitlab command.

        Args:
            tail: The tail of the command.
        """
        self._forge_quick_look(self.GitLabCommand, tail)

    class BitBucketCommand(ForgeCommand):
        """The BitBucket quick load command."""

    def command_bitbucket(self, tail: str) -> None:
        """The BitBucket command.

        Args:
            tail: The tail of the command.
        """
        self._forge_quick_look(self.BitBucketCommand, tail)

    class CodebergCommand(ForgeCommand):
        """The Codeberg quick load command."""

    def command_codeberg(self, tail: str) -> None:
        """The Codeberg command.

        Args:
            tail: The tail of the command.
        """
        self._forge_quick_look(self.CodebergCommand, tail)

    def command_discord(self, _: str) -> None:
        """The command to visit the Textualize discord server."""
        open_url(DISCORD)

    def command_changelog(self, _: str) -> None:
        """The command to show the application's own ChangeLog"""
        self.command_github(f"{ORGANISATION_NAME}/{PACKAGE_NAME} ChangeLog.md")

    def command_obsidian(self, vault: str) -> None:
        """The command to visit an obsidian vault, if one can be seen.

        Args:
            vault: The vault to visit.

        If the vault name is empty, an attempt will be made to visit the
        root level of all Obsidian vaults.

        Note:
            At the moment this will only work with Obsidian on macOS where
            the vaults are being held in iCloud.
        """
        # Right now this will only work on macOS. I've not used Obsidian on
        # any other OS so I'm unsure where the vault will be stored. I'll
        # add to this once I've found out.
        if (
            target := (
                Path(
                    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents"
                ).expanduser()
                / vault
            )
        ).exists():
            self.command_chdir(str(target))
