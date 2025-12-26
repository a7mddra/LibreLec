import sys
from pathlib import Path

class SystemUtils:
    @staticmethod
    def get_documents_path():
        """Returns the user's Documents folder cross-platform."""
        if sys.platform == "win32":
            import ctypes.wintypes
            CSIDL_PERSONAL = 5       # My Documents
            SHGFP_TYPE_CURRENT = 0   # Get current, not default value
            buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
            return Path(buf.value)
        else:
            return Path.home() / "Documents"
