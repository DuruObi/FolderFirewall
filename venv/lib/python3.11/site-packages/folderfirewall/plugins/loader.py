# backend/plugins/loader.py

import importlib
import pkgutil
from plugins.base import Plugin
import os

# Set the package path explicitly
package_path = os.path.dirname(__file__)

def load_plugins():
    plugins = []

    for _, module_name, _ in pkgutil.iter_modules([package_path]):
        if module_name in ("base", "loader"):
            continue

        module = importlib.import_module(f"plugins.{module_name}")

        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, type) and issubclass(obj, Plugin) and obj is not Plugin:
                plugins.append(obj())

    return plugins
