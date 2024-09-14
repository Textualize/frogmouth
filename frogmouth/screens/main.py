"""The main screen for the application."""

from __future__ import annotations

from functools import partial
from pathlib import Path
from typing import Awaitable, Callable
from webbrowser import open as open_url

from httpx import URL
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.events import Paste
from textual.screen import Screen
from textual.widgets import Footer, Markdown

from .. import __version__
from ..data import load_config, load_history, save_config, save_history
from ..dialogs import ErrorDialog, HelpDialog, InformationDialog, InputDialog
from ..utility import (
    build_raw_bitbucket_url,
    build_raw_codeberg_url,
    build_raw_github_url,
    build_raw_gitlab_url,
    is_likely_url,
    maybe_markdown,
)
from ..utility.advertising import (
    APPLICATION_TITLE,
    ORGANISATION_NAME,
    ORGANISATION_TITLE,
    ORGANISATION_URL,
    PACKAGE_NAME,
    TEXTUAL_URL,
)
from ..widgets import Navigation, Omnibox, Viewer
from ..widgets.navigation_panes import Bookmarks, History, LocalFiles


class Main(Screen[None]):  # pylint:disable=too-many-public-methods
    """The main screen for the application."""

    DEFAULT_CSS = """
    .focusable {
        border: blank;
    }

    .focusable:focus {
        border: heavy $accent !important;
    }


    Screen Tabs {
        border: blank;
        height: 5;
    }

    Screen Tabs:focus {
        border: heavy $accent !important;
        height: 5;
    }

    Screen TabbedContent TabPane {
        padding: 0 1;
        border: blank;
    }

    Screen TabbedContent TabPane:focus-within {
        border: heavy $accent !important;
    }
    """

    BINDINGS = [
        Binding("/,:", "omnibox", "Omnibox", show=False),
        Binding("ctrl+b", "bookmarks", "", show=False),
        Binding("ctrl+d", "bookmark_this", "", show=False),
        Binding("ctrl+l", "local_files", "", show=False),
        Binding("ctrl+left", "backward", "", show=False),
        Binding("ctrl+right", "forward", "", show=False),
        Binding("ctrl+r", "reload", "", show=False),
        Binding("ctrl+t", "table_of_contents", "", show=False),
        Binding("ctrl+y", "history", "", show=False),
        Binding("escape", "escape", "", show=False),
        Binding("f1", "help", "Help"),
        Binding("f2", "about", "About"),
        Binding("ctrl+n", "navigation", "Navigation"),
        Binding("ctrl+q", "app.quit", "Quit"),
        Binding("f10", "toggle_theme", "", show=False),
    ]
    """The keyboard bindings for the main screen."""

    def __init__(self, initial_location: str | None = None) -> None:
        """Initialise the main screen.

        Args:
            initial_location: The initial location to view.
        """
        super().__init__()
        self._initial_location = initial_location

    def compose(self) -> ComposeResult:
        """Compose the main screen.

        Returns:
            The result of composing the screen.
        """
        yield Omnibox(classes="focusable")
        with Horizontal():
            yield Navigation()
            yield Viewer(classes="focusable")
        yield Footer()

    def visit(self, location: Path | URL, remember: bool = True, focus:bool = True) -> None:
        """Visit the given location.

        Args:
            location: The location to visit.
            remember: Should the visit be added to the history?
        """
        # If the location we've been given looks like it is markdown, be it
        # locally in the filesystem or out on the web...
        if maybe_markdown(location):
            # ...attempt to visit it in the viewer.
            self.query_one(Viewer).visit(location, remember, focus)
        elif isinstance(location, Path):
            # So, it's not Markdown, but it *is* a Path of some sort. If the
            # resource seems to exist...
            if location.exists():
                # ...ask the OS to open it.
                open_url(f"file:///{location.absolute()}")
            else:
                # It's a Path but it doesn't exist, there's not much else we
                # can do with it.
                self.app.push_screen(
                    ErrorDialog(
                        "Does not exist",
                        f"Unable to open {location} because it does not exist.",
                    )
                )
        else:
            # By this point all that's left is it's a URL that, on the
            # surface, doesn't look like a Markdown file. Let's hand off to
            # the operating system anyway.
            open_url(str(location), new=2, autoraise=True)

    async def on_mount(self) -> None:
        """Set up the main screen once the DOM is ready."""

        # Currently Textual's Markdown can steal focus, which gets confusing
        # as it's not obvious *what* is focused. So let's stop it from
        # allowing the content to get focus.
        #
        # https://github.com/Textualize/textual/issues/2380
        self.query_one(Markdown).can_focus_children = False

        # Load up any history that might be saved.
        if history := load_history():
            self.query_one(Viewer).load_history(history)

        # If we've not been tasked to start up looking at a very specific
        # location (in other words if no location was passed on the command
        # line), and if there is some history...
        if self._initial_location is None and history:
            # ...start up revisiting the last location the user was looking
            # at.
            self.query_one(Viewer).visit(history[-1], remember=False)
            self.query_one(Omnibox).value = str(history[-1])
        elif self._initial_location is not None:
            # Seems there is an initial location; so let's start up looking
            # at that.
            (omnibox := self.query_one(Omnibox)).value = self._initial_location
            await omnibox.action_submit()

    def on_navigation_hidden(self) -> None:
        """React to the navigation sidebar being hidden."""
        self.query_one(Viewer).focus()

    def on_omnibox_local_view_command(self, event: Omnibox.LocalViewCommand) -> None:
        """Handle the omnibox asking us to view a particular file.

        Args:
            event: The local view command event.
        """
        self.visit(event.path)

    def on_omnibox_remote_view_command(self, event: Omnibox.RemoteViewCommand) -> None:
        """Handle the omnibox asking us to view a particular URL.

        Args:
            event: The remote view command event.
        """
        self.visit(event.url)

    def on_omnibox_contents_command(self) -> None:
        """Handle being asked to show the table of contents."""
        self.action_table_of_contents()

    def on_omnibox_local_files_command(self) -> None:
        """Handle being asked to view the local files picker."""
        self.action_local_files()

    def on_omnibox_bookmarks_command(self) -> None:
        """Handle being asked to view the bookmarks."""
        self.action_bookmarks()

    def on_omnibox_local_chdir_command(self, event: Omnibox.LocalChdirCommand) -> None:
        """Handle being asked to view a new directory in the local files picker.

        Args:
            event: The chdir command event to handle.
        """
        if not event.target.exists():
            self.app.push_screen(
                ErrorDialog("No such directory", f"{event.target} does not exist.")
            )
        elif not event.target.is_dir():
            self.app.push_screen(
                ErrorDialog("Not a directory", f"{event.target} is not a directory.")
            )
        else:
            self.query_one(Navigation).jump_to_local_files(event.target)

    def on_omnibox_history_command(self) -> None:
        """Handle being asked to view the history."""
        self.action_history()

    async def _from_forge(
        self,
        forge: str,
        event: Omnibox.ForgeCommand,
        builder: Callable[[str, str, str | None, str | None], Awaitable[URL | None]],
    ) -> None:
        """Build a URL for getting a file from a given forge.

        Args:
            forge: The display name of the forge.
            event: The event that contains the request information for the file.
            builder: The function that builds the URL.
        """
        if url := await builder(
            event.owner, event.repository, event.branch, event.desired_file
        ):
            self.visit(url)
        else:
            self.app.push_screen(
                ErrorDialog(
                    f"Unable to work out a {forge} URL",
                    f"After trying a few options it hasn't been possible to work out the {forge} URL.\n\n"
                    "Perhaps the file you're after is on an unusual branch, or the spelling is wrong?",
                )
            )

    async def on_omnibox_git_hub_command(self, event: Omnibox.GitHubCommand) -> None:
        """Handle a GitHub file shortcut command.

        Args:
            event: The GitHub shortcut command event to handle.
        """
        await self._from_forge("GitHub", event, build_raw_github_url)

    async def on_omnibox_git_lab_command(self, event: Omnibox.GitLabCommand) -> None:
        """Handle a GitLab file shortcut command.

        Args:
            event: The GitLab shortcut command event to handle.
        """
        await self._from_forge("GitLab", event, build_raw_gitlab_url)

    async def on_omnibox_bit_bucket_command(
        self, event: Omnibox.BitBucketCommand
    ) -> None:
        """Handle a BitBucket shortcut command.

        Args:
            event: The BitBucket shortcut command event to handle.
        """
        await self._from_forge("BitBucket", event, build_raw_bitbucket_url)

    async def on_omnibox_codeberg_command(self, event: Omnibox.CodebergCommand) -> None:
        """Handle a Codeberg shortcut command.

        Args:
            event: The Codeberg shortcut command event to handle.
        """
        await self._from_forge("Codeberg", event, build_raw_codeberg_url)

    def on_omnibox_about_command(self) -> None:
        """Handle being asked to show the about dialog."""
        self.action_about()

    def on_omnibox_help_command(self) -> None:
        """Handle being asked to show the help document."""
        self.action_help()

    def on_omnibox_quit_command(self) -> None:
        """Handle being asked to quit."""
        self.app.exit()

    def on_local_files_goto(self, event: LocalFiles.Goto) -> None:
        """Visit a local file in the viewer.

        Args:
            event: The local file visit request event.
        """
        self.visit(event.location , focus=event.focus_viewer)

    def on_history_goto(self, event: History.Goto) -> None:
        """Handle a request to go to a location from history.

        Args:
            event: The event to handle.
        """
        self.visit(
            event.location, remember=event.location != self.query_one(Viewer).location
        )

    def on_history_delete(self, event: History.Delete) -> None:
        """Handle a request to delete an item from history.

        Args:
            event: The event to handle.
        """
        self.query_one(Viewer).delete_history(event.history_id)

    def on_history_clear(self) -> None:
        """handle a request to clear down all of history."""
        self.query_one(Viewer).clear_history()

    def on_bookmarks_goto(self, event: Bookmarks.Goto) -> None:
        """Handle a request to go to a bookmark.

        Args:
            event: The event to handle.
        """
        self.visit(event.bookmark.location)

    def on_viewer_location_changed(self, event: Viewer.LocationChanged) -> None:
        """Update for the location being changed.

        Args:
            event: The location change event.
        """
        # Update the omnibox with whatever is appropriate for the new location.
        self.query_one(Omnibox).visiting = (
            str(event.viewer.location) if event.viewer.location is not None else ""
        )
        # Having safely arrived at a new location, that implies that we want
        # to focus on the viewer.
        self.query_one(Viewer).focus()

    def on_viewer_history_updated(self, event: Viewer.HistoryUpdated) -> None:
        """Handle the viewer updating the history.

        Args:
            event: The history update event.
        """
        self.query_one(Navigation).history.update_from(event.viewer.history.locations)
        save_history(event.viewer.history.locations)

    def on_markdown_table_of_contents_updated(
        self, event: Markdown.TableOfContentsUpdated
    ) -> None:
        """Handle the table of contents of the document being updated.

        Args:
            event: The table of contents update event to handle.
        """
        # We don't handle this, the navigation pane does. Bounce the event
        # over there.
        self.query_one(Navigation).table_of_contents.on_table_of_contents_updated(event)

    def on_markdown_table_of_contents_selected(
        self, event: Markdown.TableOfContentsSelected
    ) -> None:
        """Handle the user selecting something from the table of contents.

        Args:
            event: The table of contents selection event to handle.
        """
        self.query_one(Viewer).scroll_to_block(event.block_id)

    def on_markdown_link_clicked(self, event: Markdown.LinkClicked) -> None:
        """Handle a link being clicked in the Markdown document.

        Args:
            event: The Markdown link click event to handle.
        """
        # We'll be using the current location to help work out some relative
        # things.
        current_location = self.query_one(Viewer).location
        # If the link we're to handle obviously looks like URL...
        if is_likely_url(event.href):
            # ...handle it as such. No point in trying to do anything else.
            self.visit(URL(event.href))
        elif isinstance(current_location, URL):
            # Seems we're currently visiting a remote location, and the href
            # looks like a simple file path, so let's make a best effort to
            # visit the file at the remote location.
            self.visit(current_location.copy_with().join(event.href))
        elif (local_file := Path(event.href)).exists():
            # It looks like a local file and it exists...
            self.visit(local_file)
        elif (
            isinstance(current_location, Path)
            and (local_file := (current_location.parent / Path(event.href)))
            .absolute()
            .exists()
        ):
            # It looks like a local file, and tested relative to the
            # document we found it exists in the local filesystem, so let's
            # assume that's what we're supposed to handle.
            self.visit(local_file)
        elif event.href.startswith("#") and event.markdown.goto_anchor(event.href[1:]):
            # The href started with a # and the remains of it were satisfied
            # as an anchor within the document of the Markdown. We should
            # have scrolled to about the right spot in the document so we
            # don't need to do anything else.
            pass
        else:
            # Yeah, not sure *what* this link is. Rather than silently fail,
            # let's let the user know we don't know how to process this.
            self.app.push_screen(
                ErrorDialog(
                    "Unable to handle link",
                    f"Unable to work out how to handle this link:\n\n{event.href}",
                )
            )

    def on_paste(self, event: Paste) -> None:
        """Handle a paste event.

        Args:
            event: The paste event.

        This method is here to capture paste events that look like the name
        of a local file (later I may add URL support too). The main purpose
        of this is to handle drag/drop into the terminal.
        """
        if (candidate_file := Path(event.text)).exists():
            self.visit(candidate_file)

    def action_navigation(self) -> None:
        """Toggle the availability of the navigation sidebar."""
        self.query_one(Navigation).toggle()

    def action_escape(self) -> None:
        """Process the escape key."""
        # Escape is designed to work backwards out of the application. If
        # the viewer is focused, the omnibox gets focused, if omnibox has
        # focus but it isn't empty, it gets emptied, if it's empty we exit
        # the application. The idea being that folk who use this often want
        # to build up muscle memory on the keyboard will know to camp on the
        # escape key until they get to where they want to be.
        if (omnibox := self.query_one(Omnibox)).has_focus:
            if omnibox.value:
                omnibox.value = ""
            else:
                self.app.exit()
        else:
            if self.query("Navigation:focus-within"):
                self.query_one(Navigation).popped_out = False
            omnibox.focus()

    def action_omnibox(self) -> None:
        """Jump to the omnibox."""
        self.query_one(Omnibox).focus()

    def action_table_of_contents(self) -> None:
        """Display and focus the table of contents pane."""
        self.query_one(Navigation).jump_to_contents()

    def action_local_files(self) -> None:
        """Display and focus the local files selection pane."""
        self.query_one(Navigation).jump_to_local_files()

    def action_bookmarks(self) -> None:
        """Display and focus the bookmarks selection pane."""
        self.query_one(Navigation).jump_to_bookmarks()

    def action_history(self) -> None:
        """Display and focus the history pane."""
        self.query_one(Navigation).jump_to_history()

    def action_backward(self) -> None:
        """Go backward in the history."""
        self.query_one(Viewer).back()

    def action_forward(self) -> None:
        """Go forward in the history."""
        self.query_one(Viewer).forward()

    def action_help(self) -> None:
        """Show the help."""
        self.app.push_screen(HelpDialog())

    def action_about(self) -> None:
        """Show the about dialog."""
        self.app.push_screen(
            InformationDialog(
                f"{APPLICATION_TITLE} [b dim]v{__version__}",
                f"Built with [@click=app.visit('{TEXTUAL_URL}')]Textual[/] "
                f"by [@click=app.visit('{ORGANISATION_URL}')]{ORGANISATION_TITLE}[/].\n\n"
                f"[@click=app.visit('https://github.com/{ORGANISATION_NAME}/{PACKAGE_NAME}')]"
                f"https://github.com/{ORGANISATION_NAME}/{PACKAGE_NAME}[/]",
            )
        )

    def add_bookmark(self, location: Path | URL, bookmark: str) -> None:
        """Handle adding the bookmark.

        Args:
            location: The location to bookmark.
            bookmark: The bookmark to add.
        """
        self.query_one(Navigation).bookmarks.add_bookmark(bookmark, location)

    def action_bookmark_this(self) -> None:
        """Add a bookmark for the currently-viewed file."""

        location = self.query_one(Viewer).location

        # Only allow bookmarking if we're actually viewing something that
        # can be bookmarked.
        if not isinstance(location, (Path, URL)):
            self.app.push_screen(
                ErrorDialog(
                    "Not a bookmarkable location",
                    "The current view can't be bookmarked.",
                )
            )
            return

        # To make a bookmark, we need a title and a location. We've got a
        # location; let's make the filename the default title.
        title = (location if isinstance(location, Path) else Path(location.path)).name

        # Give the user a chance to edit the title.
        self.app.push_screen(
            InputDialog("Bookmark title:", title),
            partial(self.add_bookmark, location),
        )

    def action_toggle_theme(self) -> None:
        """Toggle the light/dark mode theme."""
        config = load_config()
        config.light_mode = not config.light_mode
        save_config(config)
        # pylint:disable=attribute-defined-outside-init
        self.app.dark = not config.light_mode

    def action_reload(self) -> None:
        """Reload the current document."""
        self.query_one(Viewer).reload()
