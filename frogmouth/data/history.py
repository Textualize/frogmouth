"""Provides code for saving and loading the history."""

from __future__ import annotations

from json import JSONEncoder, dumps, loads
from pathlib import Path
from typing import Any

from httpx import URL

from ..utility import is_likely_url
from .data_directory import data_directory


def history_file() -> Path:
    """Get the location of the history file.

    Returns:
        The location of the history file.
    """
    return data_directory() / "history.json"


class HistoryEncoder(JSONEncoder):
    """JSON encoder for the history data."""

    def default(self, o: object) -> Any:
        """Handle the Path and URL values.

        Args:
            o: The object to handle.

        Return:
            The encoded object.
        """
        return str(o) if isinstance(o, (Path, URL)) else o


def save_history(history: list[Path | URL]) -> None:
    """Save the given history.

    Args:
        history: The history to save.
    """
    history_file().write_text(dumps(history, indent=4, cls=HistoryEncoder))


def load_history() -> list[Path | URL]:
    """Load the history.

    Returns:
        The history.
    """
    return (
        [
            URL(location) if is_likely_url(location) else Path(location)
            for location in loads(history.read_text())
        ]
        if (history := history_file()).exists()
        else []
    )
