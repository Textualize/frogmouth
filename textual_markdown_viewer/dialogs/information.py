"""Provides an information dialog."""

from .text_dialog import TextDialog


class InformationDialog(TextDialog):
    """Modal dialog that shows information."""

    DEFAULT_CSS = """
    InformationDialog > Vertical {
        border: thick $primary 50%;
    }
    """
