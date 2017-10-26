"""Utilities for working with M-O task files."""

from pathlib import Path
import yaml

from .project import Project


def load(filename):
    """Load a M-O task file and get a ``Project`` back."""

    path = Path(filename).resolve()

    with path.open() as file:
        config = yaml.load(file.read())

    return Project(config, path.parent)
