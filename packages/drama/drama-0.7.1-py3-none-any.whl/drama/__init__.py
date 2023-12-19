"""
====================================
DRAMA Documentation (:mod:`drama`)
====================================

.. currentmodule:: DRAMA

DRAMA: Delft RAdar Modeling and Performance Analysis
"""
from importlib.metadata import version

try:
    __version__ = version("drama")
except Exception:
    # Local copy or not installed with setuptools.
    # Disable minimum version checks on downstream libraries.
    # Exception handling taken from xarray
    __version__ = "999"
