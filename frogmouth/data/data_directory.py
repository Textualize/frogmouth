"""Provides a function for working out the data directory location."""
import os
from pathlib import Path

from xdg import xdg_data_home

from ..utility.advertising import ORGANISATION_NAME, PACKAGE_NAME


def data_directory() -> Path:
    """Get the location of the data directory.

    The location of the configfile can be explicitly set by the
    environment variable ``FROGMOUTH_DATA_DIR``.
    When this env-var is not set, we default to XDG-directories.

    Returns:
        The location of the data directory.

    Note:
        As a side effect, if the xdg-directory doesn't exist it will be created.
    """

    if target_directory := os.getenv("FROGMOUTH_DATA_DIR"):
        return Path(target_directory)

    (target_directory := xdg_data_home() / ORGANISATION_NAME / PACKAGE_NAME).mkdir(
        parents=True, exist_ok=True
    )
    return target_directory
