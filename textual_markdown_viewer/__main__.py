"""The main entry points for the application.

This module provides both a 'python -m' entry point, and a `main` function
that can be called upon from an executable script.
"""

from .app import run

if __name__ == "__main__":
    run()
