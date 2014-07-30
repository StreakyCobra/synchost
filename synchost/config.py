# -*- coding: utf-8 -*-
"""Manage the configuration of synchost."""

import os

# Set some paths
home_path     = os.environ.get('HOME')
xdg_path      = os.environ.get('XDG_CONFIG_HOME',
                               os.path.join(home_path, '.config'))
synchost_path = os.path.join(xdg_path, 'synchost')
plugins_path = os.path.join(synchost_path, 'plugins')

# Ensure groupman config folder is existing
if not os.path.isdir(synchost_path):
    os.makedirs(synchost_path)

# Ensure plugins folder is existing
if not os.path.isdir(plugins_path):
    os.makedirs(plugins_path)
