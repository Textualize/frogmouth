"""Provides the history navigation pane."""

from __future__ import annotations

from functools import partial
from pathlib import Path

from httpx import URL
from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.message import Message
from textual.widgets import OptionList
from textual.widgets.option_list import Option

from ...dialogs import YesNoDialog
from .navigation_pane import NavigationPane


class Entry(Option):
    """An entry in the history."""

    def __init__(self, history_id: int, location: Path | URL) -> None:
        """Initialise the history entry item.

        Args:
            history_id: The ID of the item of history.
            location: The location being added to history.
        """
        super().__init__(self._as_prompt(location))
        self.history_id = history_id
        """The ID of the item of history."""
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
                f":page_facing_up: [bold]{location.name}[/]\n[dim]{location.parent}[/]",
                overflow="ellipsis",
            )
        return Text.from_markup(
            f":globe_with_meridians: [bold]{Path(location.path).name}[/]"
            f"\n[dim]{Path(location.path).parent}\n{location.host}[/]",
            overflow="ellipsis",
        )


class History(NavigationPane):
    """History navigation pane."""

    DEFAULT_CSS = """
    History {
        height: 100%;
    }

    History > OptionList {
        background: $panel;
    }
    """

    BINDINGS = [Binding("delete", "delete", "Delete the history item")]
    """The bindings for the history navigation pane."""

    def __init__(self) -> None:
        """Initialise the history navigation pane."""
        super().__init__("History")

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield OptionList()

    def set_focus_within(self) -> None:
        """Focus the option list."""
        self.query_one(OptionList).focus(scroll_visible=False)

    def update_from(self, locations: list[Path | URL]) -> None:
        """Update the history from the given list of locations.

        Args:
            locations: A list of locations to update the history with.

        This call removes any existing history and sets it to the given
        value.
        """
        option_list = self.query_one(OptionList).clear_options()
        for history_id, location in reversed(list(enumerate(locations))):
            option_list.add_option(Entry(history_id, location))

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

    class Delete(Message):
        """Message that requests the viewer to delete an item of history."""

        def __init__(self, history_id: int) -> None:
            """initialise the history delete message.

            args:
                history_id: The ID of the item of history to delete.
            """
            super().__init__()
            self.history_id = history_id
            """The ID of the item of history to delete."""

    def delete_history(self, history_id: int, delete_it: bool) -> None:
        """Delete a given history entry.

        Args:
            history_id: The ID of the item of history to delete.
            delete_it: Should it be deleted?
        """
        if delete_it:
            self.post_message(self.Delete(history_id))

    def action_delete(self) -> None:
        """Delete the highlighted item from history."""
        history = self.query_one(OptionList)
        if (item := history.highlighted) is not None:
            entry = history.get_option_at_index(item)
            assert isinstance(entry, Entry)
            self.app.push_screen(
                YesNoDialog(
                    "Delete history entry?",
                    "Are you sure you want to delete the history entry?",
                ),
                partial(self.delete_history, entry.history_id),
            )
