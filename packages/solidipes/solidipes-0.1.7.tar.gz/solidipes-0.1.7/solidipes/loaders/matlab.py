from .. import viewers
from .file import File


class MatlabData(File):
    """Matlab .mat file"""

    initial_data_collection_keys = File.initial_data_collection_keys + ["arrays"]
    supported_mime_types = ["application/x-matlab-data"]
    supported_file_extensions = ["mat"]

    def __init__(self, path):
        super().__init__(path)
        self.default_viewer = viewers.MatlabData

    def _load_data(self, key):
        """Read full text file"""

        data = super()._load_data(key)
        if data is not None:
            return data

        mat = None
        if key == "arrays":
            import scipy.io

            mat = scipy.io.loadmat(self.file_info.path)
        return mat
