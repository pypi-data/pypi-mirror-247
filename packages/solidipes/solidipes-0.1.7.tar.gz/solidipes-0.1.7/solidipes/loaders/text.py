from .. import viewers
from .file import File


class Text(File):
    """Text file, potentially formatted with markdown"""

    initial_data_collection_keys = File.initial_data_collection_keys + ["text"]
    supported_mime_types = ["text/plain"]
    supported_file_extensions = ["txt"]

    def __init__(self, path):
        super().__init__(path)
        self.default_viewer = viewers.Text

    def _load_data(self, key):
        """Read full text file"""

        data = super()._load_data(key)
        if data is not None:
            return data

        text = ""
        with open(self.file_info.path, "r") as f:
            text = f.read()
        return text


class Markdown(Text):
    """Markdown file"""

    supported_mime_types = ["text/markdown"]
    supported_file_extensions = ["md"]

    def __init__(self, path):
        super().__init__(path)
        self.default_viewer = viewers.MarkdownViewer
