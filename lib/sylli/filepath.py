#!/usr/bin/env python
#----------------------------------------------------------------------------
# Name:         __init__.py
# Purpose:      Config handler
#
# Author:       Luca Iacoponi
#
# Created:      July 2010
# Licence:      GNU GPL license
# Credits:      Some code from BitTorrent4.0 configfile.py
#----------------------------------------------------------------------------

""" a cross-platform way to get user's home directory """

import sys
import os

def get_config_dir():
    """ Get config dir on Windows

    >>> get_config_dir()
    C:\\Users\\nijan\\AppData\\Roaming
    """
    shellvars = ['${APPDATA}', '${HOME}', '${USERPROFILE}']
    return get_dir_root(shellvars)

def get_home_dir():
    """ Get home directory

    >>> get_home_dir()
    '/home/alice'
    """
    shellvars = ['${HOME}', '${USERPROFILE}']
    return get_dir_root(shellvars)

def get_dir_root(shellvars):
    """ Get root directory of a env var

    >>> get_dir_root('${HOME}')
    '/home/alice'
    """

    def check_sysvars(sysvar):
        """ Check if sysvars exist and return it """
        exp = os.path.expandvars(sysvar)
        if exp != sysvar and os.path.isdir(exp):
            return exp
        return None

    dir_root = None
    for sysv in shellvars:
        dir_root = check_sysvars(sysv)
        if dir_root is not None:
            break
    else:
        dir_root = os.path.expanduser('~')
        if dir_root == '~' or not os.path.isdir(dir_root):
            dir_root = None
    return dir_root

def get_path(path):
    """ Get a path of a specific sylli's location

    >>> get_path('config_dir')
    '/home/alice/.sylli'
    >>> get_path('inst_sonority')
    '/home/alice/Sylli/sylli/config/sonority.txt'
    >>> get_path('usr_sonority')
    '/home/alice/.sylli/sonority.txt'
    >>> get_path('images')
    '/home/alice/Sylli/sylli/images'
    """
    # User directories
    if os.name == 'nt':
        config = get_config_dir() + '\Sylli'
    else:
        config = get_home_dir() + '/.sylli'

    app_root = os.path.split(os.path.abspath(sys.argv[0]))[0]
    conf_root = os.path.join(app_root, 'config')

    if path == 'config_dir':
        return config
    if path == 'usr_sonority':
        return os.path.join(config, 'sonority.txt')
    if path == 'inst_sonority':
        return os.path.join(conf_root, 'sonority.txt')
    if path == 'images':
        return os.path.join(app_root, 'images')
    if path == 'htmldoc':
        return os.path.join(app_root, 'htmldoc')
