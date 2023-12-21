from .. import viewers
from ..utils import load_file
from .data_container import DataContainer
from .file import File
from .mime_types import get_extension, get_mime_type


class SymLink(File):
    """Symbolic link (special file)"""

    initial_data_collection_keys = File.initial_data_collection_keys + ["linked_file"]

    def __init__(self, path):
        super().__init__(path)
        self.default_viewer = viewers.SymLink

    def _load_data(self, key):
        """Load file_info"""

        if key == "file_info":
            import os

            stats = os.lstat(self.path)
            mime_type, charset = get_mime_type(self.path)
            return DataContainer(
                {
                    "size": stats.st_size,
                    "created_time": stats.st_ctime,
                    "modified_time": stats.st_mtime,
                    "permissions": stats.st_mode,
                    "owner": stats.st_uid,
                    "group": stats.st_gid,
                    "path": self.path,
                    "type": mime_type,
                    "charset": charset,
                    "extension": get_extension(self.path),
                }
            )

        if key == "linked_file":
            from pathlib import Path

            _path = Path(self.file_info.path).resolve()
            if os.path.exists(_path):
                return load_file(_path)
            return _path

        data = super()._load_data(key)
        if data is not None:
            return data
