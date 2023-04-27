"""The main help dialog for the application."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Markdown
from typing_extensions import Final

from ..utility.advertising import APPLICATION_TITLE

HELP: Final[
    str
] = f"""\
# {APPLICATION_TITLE} Help

## Keys

### Navigation keys:

| Key | Command |
| -- | -- |
| `Ctrl+n` | Show/hide the navigation |
| `Ctrl+b` | Show the bookmarks |
| `Ctrl+l` | Show the local file browser |
| `Ctrl+t` | Show the table of contents |
| `Ctrl+y` | Show the history |
| `Ctrl+left` | Go backward in history |
| `Ctrl+right` | Go forward in history |


### General keys:

| Key | Command |
| -- | -- |
| `Ctrl+d` | Add the current document to the bookmarks |
| `F10` | Toggle dark/light theme |

## Commands

| Command | Aliases | Arguments | Command |
| -- | -- | -- | -- |
| `about` | `a` | | Show details about the application |
| `bookmarks` | `b`, `bm` | | Show the bookmarks list |
| `bitbucket` | `bb` | `<repo-info>` | View a file on BitBucket (see below) |
| `chdir` | `cd` | `<dir>` | Switch the local file browser to a new directory |
| `contents` | `c`, `toc` | | Show the table of contents for the document |
| `discord` | | | Visit the Textualize Discord server |
| `github` | `gh` | `<repo-info>` | View a file on GitHub (see below) |
| `gitlab` | `gl` | `<repo-info>` | View a file on GitLab (see below) |
| `help` | `?` | | Show this document |
| `history` | `h` | | Show the history |
| `local` | `l` | | Show the local file browser |
| `quit` | `q` | | Quit the viewer |

## Git forge quick view

The git forge quick view command can be used to quickly view a file on a git
forge such as GitHub or GitLab. Various forms of specifying the repository,
branch and file are supported. For example:

- `<owner>`/`<repo>`
- `<owner>`/`<repo>` `<file>`
- `<owner>` `<repo>`
- `<owner>` `<repo>` `<file>`
- `<owner>`/`<repo>`:`<branch>`
- `<owner>`/`<repo>`:`<branch>` `<file>`
- `<owner>` `<repo>`:`<branch>`
- `<owner>` `<repo>`:`<branch>` `<file>`

Anywhere where `<file>` is omitted it is assumed `README.md` is desired.

Anywhere where `<branch>` is omitted a test is made for the desired file on
first a `main` and then a `master` branch.
"""
"""The main help text for the application."""


class HelpDialog(ModalScreen[None]):
    """Modal dialog that shows the application's help."""

    DEFAULT_CSS = """
    HelpDialog {
        align: center middle;
    }

    HelpDialog > Vertical {
        border: thick $primary 50%;
        width: 80%;
        height: 80%;
        background: $panel;
    }

    HelpDialog > Vertical > VerticalScroll {
        height: 1fr;
    }

    HelpDialog > Vertical > Center {
        border-top: solid $primary;
        padding: 1;
        height: auto;
    }
    """

    BINDINGS = [
        Binding("escape,f1", "dismiss(None)", "", show=False),
    ]
    """Bindings for the help dialog."""

    def compose(self) -> ComposeResult:
        """Compose the help screen."""
        with Vertical():
            with VerticalScroll():
                yield Markdown(HELP)
            with Center():
                yield Button("Close", variant="primary")

    def on_mount(self) -> None:
        """Configure the help screen once the DOM is ready."""
        # It seems that some things inside Markdown can still grab focus;
        # which might not be right. Let's ensure that can't happen here.
        self.query_one(Markdown).can_focus_children = False
        self.query_one("Vertical > VerticalScroll").focus()

    def on_button_pressed(self) -> None:
        """React to button press."""
        self.dismiss(None)
