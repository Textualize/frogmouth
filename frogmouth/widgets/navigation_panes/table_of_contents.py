"""Provides the table of contents navigation pane."""

from textual.app import ComposeResult
from textual.widgets import Markdown, Tree
from textual.widgets.markdown import MarkdownTableOfContents

from .navigation_pane import NavigationPane


class TableOfContents(NavigationPane):
    """Markdown document table of contents navigation pane."""

    DEFAULT_CSS = """
    TableOfContents {
        height: 100%;
    }

    TableOfContents > MarkdownTableOfContents {
        background: $panel;
        border: none;
    }

    TableOfContents > MarkdownTableOfContents > Tree {
        width: 1fr;
        background: $panel;
        padding: 0;
    }

    TableOfContents > MarkdownTableOfContents > Tree:focus .tree--cursor, TableOfContents > MarkdownTableOfContents > Tree .tree--cursor {
        background: $accent 50%;
        color: $text;
    }
    """

    def __init__(self) -> None:
        """Initialise the table of contents navigation pane."""
        super().__init__("Contents")

    def set_focus_within(self) -> None:
        """Ensure the tree in the table of contents is focused."""
        self.query_one("MarkdownTableOfContents > Tree", Tree).focus(
            scroll_visible=False
        )

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        # Note the use of a throwaway Markdown object. Textual 0.24
        # introduced a requirement for MarkdownTableOfContents to take a
        # reference to a Markdown document; this is a problem if you're
        # composing the ToC in a location somewhere unrelated to the
        # document itself, such that you can't guarantee the order in which
        # they're compose. I'm not using the ToC in a way that's
        # tightly-coupled to the document, neither am I using multiple ToCs
        # and documents. So... we make one and ignore it.
        #
        # https://github.com/Textualize/textual/issues/2516
        yield MarkdownTableOfContents(Markdown())

    def on_table_of_contents_updated(
        self, event: Markdown.TableOfContentsUpdated
    ) -> None:
        """Handle a table of contents update event.

        Args:
            event: The table of content update event to handle.
        """
        self.query_one(
            MarkdownTableOfContents
        ).table_of_contents = event.table_of_contents
