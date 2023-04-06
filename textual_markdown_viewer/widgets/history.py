"""Provides the history navigation pane."""

from __future__ import annotations

from pathlib import Path

from httpx import URL

from rich.text import Text


from textual.app import ComposeResult
from textual.message import Message
from textual.widgets import OptionList
from textual.widgets.option_list import Option

from .navigatgion_pane import NavigationPane


class Entry(Option):
    """An entry in the history."""

    def __init__(self, location: Path | URL) -> None:
        """Initialise the history entry item.

        Args:
            location: The location being added to history.
        """
        super().__init__(self._as_prompt(location))
        self.location = location
        """The location for his entry in the history."""

    @staticmethod
    def _as_prompt(location: Path | URL) -> Text:
        """Depict the location as a decorated prompt.

        Args:
            location: The location to depict.

        Returns:
            A prompt with icon, etc.
        """
        if isinstance(location, Path):
            return Text.from_markup(
                f":page_facing_up: {location.name}\n{location.parent}",
                overflow="ellipsis",
            )
        return Text.from_markup(
            f":globe_with_meridians: {Path(location.path).name}"
            f"\n{Path(location.path).parent}\n{location.host}",
            overflow="ellipsis",
        )


class History(NavigationPane):
    """History navigation pane."""

    DEFAULT_CSS = """
    History {
        height: 100%;
    }

    History > OptionList {
        background: $primary;
    }
    """

    def __init__(self) -> None:
        """Initialise the history navigation pane."""
        super().__init__("History")

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield OptionList()

    def set_focus_within(self) -> None:
        """Focus the option list."""
        self.query_one(OptionList).focus()

    def add(self, location: Path | URL) -> None:
        """Add a new location to the history.

        Args:
            location: The location to add.
        """
        self.query_one(OptionList).add_option(Entry(location))

    class Goto(Message):
        """Message that requests the viewer goes to a given location."""

        def __init__(self, location: Path | URL) -> None:
            """Initialise the history goto message.

            Args:
                location: The location to go to.
            """
            super().__init__()
            self.location = location
            """The location to go to."""

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle an entry in the history being selected.

        Args:
            event: The event to handle.
        """
        event.stop()
        assert isinstance(event.option, Entry)
        self.post_message(self.Goto(event.option.location))
