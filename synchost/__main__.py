# -*- coding: utf-8 -*-

import os
import sys
import importlib

from synchost.config import plugins_path

sys.path.insert(0, plugins_path)


def load_module(module_name):
    """Load and return a module dynamically from its name."""
    # Load the module dynamically
    mod = importlib.import_module(module_name)
    # Return the module
    return mod


def exec_plugin(filename):
    name = os.path.splitext(filename)[0]
    plugin = load_module(name)
    print("%s: %d" % (name, plugin.status()))


def run():
    for filename in os.listdir(plugins_path):
        if os.path.isfile(os.path.join(plugins_path, filename)):
            exec_plugin(filename)


# When used as a script
if __name__ == "__main__":
    run()
