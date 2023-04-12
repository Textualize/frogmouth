"""Provides the main help text for the application."""

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
| `Ctrl+b` | Show the bookmarks |
| `Ctrl+l` | Show the local file browser |
| `Ctrl+t` | Show the table of contents |
| `Ctrl+y` | Show the history |


### History keys:

| Key | Command |
| -- | -- |
| `Ctrl+left` | Go backward in history |
| `Ctrl+right` | Go forward in history |

## Commands

| Command | Aliases | Arguments | Command |
| -- | -- | -- | -- |
| `about` | `a` | | Show details about the application |
| `bitbucket` | `bb` | `<repo-info>` | View a file on BitBucket (see below). |
| `chdir` | `cd` | `<dir>` | Switch the local file browser to a new directory |
| `contents` | `c`, `toc` | | Show the table of contents for the document |
| `github` | `gh` | `<repo-info>` | View a file on GitHub (see below). |
| `gitlab` | `gl` | `<repo-info>` | View a file on GitLab (see below). |
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
"""The main help text for the markdown viewer application."""
