"""Small, isolated wrappers around the Windows window-message API."""

import ctypes
from ctypes import wintypes
import sys


WM_CLOSE = 0x0010


def request_window_close(pid: int) -> int:
    """Post WM_CLOSE to every top-level window owned by *pid*.

    Return the number of windows that accepted the message. Posting WM_CLOSE
    is the Windows equivalent of asking a window to close; the application may
    show a save prompt, ignore the request, or take time to exit.
    """
    if sys.platform != "win32":
        return 0

    user32 = ctypes.WinDLL("user32", use_last_error=True)
    enum_windows_callback = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    user32.EnumWindows.argtypes = [enum_windows_callback, wintypes.LPARAM]
    user32.EnumWindows.restype = wintypes.BOOL
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    user32.GetWindowThreadProcessId.restype = wintypes.DWORD
    user32.PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    user32.PostMessageW.restype = wintypes.BOOL

    posted_count = 0

    @enum_windows_callback
    def close_matching_window(hwnd, _lparam):
        nonlocal posted_count
        window_pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(window_pid))
        if window_pid.value == pid and user32.PostMessageW(hwnd, WM_CLOSE, 0, 0):
            posted_count += 1
        return True

    if not user32.EnumWindows(close_matching_window, 0):
        error_code = ctypes.get_last_error()
        if error_code:
            raise OSError(error_code, "Could not enumerate Windows application windows")

    return posted_count
