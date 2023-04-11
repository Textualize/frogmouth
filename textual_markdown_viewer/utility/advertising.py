"""Provides the 'branding' for the application."""

from .. import __version__

ORGANISATION_NAME = "textualize"
"""The organisation name to use when creating namespaced resources."""

PACKAGE_NAME = "textual-markdown-viewer"
"""The name of the package."""

APPLICATION_TITLE = "Textual Markdown Viewer"
"""The title of the application."""

USER_AGENT = f"{PACKAGE_NAME} v{__version__}"
"""The user agent to use when making web requests."""
