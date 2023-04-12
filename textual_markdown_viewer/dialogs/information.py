"""Provides an information dialog."""

from .dialog import ModalDialog


class InformationDialog(ModalDialog):
    """Modal dialog that shows information."""

    DEFAULT_CSS = """
    InformationDialog > Vertical {
        border: thick $primary 50%;
    }
    """
