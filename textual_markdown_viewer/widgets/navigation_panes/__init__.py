"""Provides the panes that go into the main navigation area."""

from .bookmarks import Bookmarks
from .history import History
from .local_files import LocalFiles
from .table_of_contents import TableOfContents

__all__ = [
    "Bookmarks",
    "History",
    "LocalFiles",
    "TableOfContents",
]
