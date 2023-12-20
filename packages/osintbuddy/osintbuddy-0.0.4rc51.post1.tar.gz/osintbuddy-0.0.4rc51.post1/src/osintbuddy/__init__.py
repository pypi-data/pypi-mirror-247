#   -------------------------------------------------------------
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
"""Python Package Template"""
from __future__ import annotations
from osintbuddy.plugins import (
    OBRegistry as Registry,
    OBPlugin as Plugin,
    OBAuthorUse as PluginUse,
    discover_plugins,
    transform,
    load_plugin,
    load_plugins
)

__version__ = "0.0.4-rc51-post1"
