import h5py

from .. import viewers
from .file import File


class HDF5(File):
    """HDF5 loader"""

    supported_mime_types = ["application/x-hdf5"]
    initial_data_collection_keys = File.initial_data_collection_keys + ["datasets"]

    def __init__(self, path):
        super().__init__(path)
        self.default_viewer = viewers.HDF5

    def _load_data(self, key):
        """Load image data with PIL"""

        data = super()._load_data(key)
        if data is not None:
            return data

        if key == "datasets":
            return h5py.File(self.file_info.path)
