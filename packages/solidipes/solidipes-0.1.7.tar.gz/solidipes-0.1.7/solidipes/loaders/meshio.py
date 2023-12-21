import meshio

from .. import viewers
from .file import File


class Meshio(File):
    """File loaded with meshio"""

    initial_data_collection_keys = File.initial_data_collection_keys + ["mesh"]

    def __init__(self, path):
        super().__init__(path)
        self.default_viewer = viewers.PyvistaPlotter

    def _load_data(self, key):
        data = super()._load_data(key)
        if data is not None:
            return data

        return meshio.read(self.file_info.path)
