import sys

def is_macos():
    return 'darwin' == sys.platform

def is_linux():
    return sys.platform.startswith('linux')

def is_windows():
    return 'win32' == sys.platform
