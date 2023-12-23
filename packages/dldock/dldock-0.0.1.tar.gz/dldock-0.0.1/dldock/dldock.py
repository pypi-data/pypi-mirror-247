import ctypes
from dldock import utils

class DlDock:
    def __init__(self, shared_lib_path:None):
        self._shared_lib = None
        self._shared_lib_path = shared_lib_path
        self.load(self._shared_lib_path)

    def shared_lib(self):
        return self._shared_lib

    def load(self, shared_lib_path):
        if utils.is_linux():
            self._shared_lib = ctypes.cdll.LoadLibrary(shared_lib_path)
            self._dlclose = ctypes.cdll.LoadLibrary('').dlclose
            self._dlclose.argtypes = [ctypes.c_void_p]
            self._dlclose.restype = ctypes.c_int
        elif utils.is_windows():
            self._shared_lib = ctypes.WinDLL(shared_lib_path)
        else:
            self._shared_lib = ctypes.cdll.LoadLibrary(shared_lib_path)

        if self._shared_lib is not None:
            self._shared_lib_handle = self._shared_lib._handle
        else:
            self._shared_lib_handle = None

    def unload(self):
        return_value = 0

        if utils.is_linux():
            return_value = self._dlclose(self._shared_lib_handle)
        elif utils.is_windows():
            ctypes.windll.kernel32.FreeLibrary(self._shared_lib_handle)
        else:
            # Do nothing.
            pass
        
        return return_value

    def reload(self):
        self.unload()
        self.load(self._shared_lib_path)
