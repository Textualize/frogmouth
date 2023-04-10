"""The main application class for the Markdown viewer."""

from argparse import Namespace, ArgumentParser

from textual.app import App
from textual import __version__ as textual_version  # pylint: disable=no-name-in-module

from .. import __version__
from ..screens import Main
from ..utility import load_config


class MarkdownViewer(App[None]):
    """The main application class."""

    TITLE = "Textual Markdown Viewer"
    """The main title for the application."""

    SUB_TITLE = f"{__version__}"
    """The sub-title for the application."""

    def __init__(self, cli_args: Namespace) -> None:
        """Initialise the application.

        Args:
            cli_args: The command line arguments.
        """
        super().__init__()
        self._args = cli_args
        self.dark = not load_config().light_mode

    def on_mount(self) -> None:
        """Set up the application after the DOM is ready."""
        self.push_screen(Main(self._args.file))


def get_args() -> Namespace:
    """Parse and return the command line arguments.

    Returns:
        The result of parsing the arguments.
    """

    # Create the parser object.
    parser = ArgumentParser(
        prog="tmv",
        description="Textual Markdown Viewer -- A Markdown viewer for the terminal.",
        epilog=f"v{__version__}",
    )

    # Add --version
    parser.add_argument(
        "-v",
        "--version",
        help="Show version information.",
        action="version",
        version=f"%(prog)s {__version__} (Textual v{textual_version})",
    )

    # The remainder is the file to view.
    parser.add_argument("file", help="The Markdown file to view", nargs="?")

    # Finally, parse the command line.
    return parser.parse_args()


def run() -> None:
    """Run the application."""
    MarkdownViewer(get_args()).run()
