"""Provides code for saving and loading bookmarks."""

from __future__ import annotations

from json import dumps, loads
from pathlib import Path
from typing import NamedTuple

from .data_directory import data_directory


class Bookmark(NamedTuple):
    """A bookmark."""

    title: str
    """The title of the bookmark."""
    location: str
    """The location of the bookmark."""


def bookmarks_file() -> Path:
    """Get the location of the bookmarks file.

    Returns:
        The location of the bookmarks file.
    """
    return data_directory() / "bookmarks.json"


def save_bookmarks(bookmarks: list[Bookmark]) -> None:
    """Save the given bookmarks.

    Args:
        bookmarks: The bookmarks to save.
    """
    bookmarks_file().write_text(dumps(bookmarks, indent=4))


def load_bookmarks() -> list[Bookmark]:
    """Load the bookmarks.

    Returns:
        The bookmarks.
    """
    return (
        [Bookmark(*bookmark) for bookmark in loads(bookmarks.read_text())]
        if (bookmarks := bookmarks_file()).exists()
        else []
    )
