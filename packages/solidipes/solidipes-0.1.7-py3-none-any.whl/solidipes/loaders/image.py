from PIL import ExifTags
from PIL import Image as PILImage
from PIL.TiffImagePlugin import IFDRational

from .. import viewers
from .data_container import DataContainer
from .file import File


class SVGWrapper:
    def __init__(self, filename):
        self.src = open(filename, "r").read()

    def _repr_svg_(self):
        return self.src

    def show(self):
        from io import BytesIO

        import cairosvg
        import matplotlib.pyplot as plt
        from PIL import Image

        img_png = cairosvg.svg2png(self.src)
        img = Image.open(BytesIO(img_png))
        plt.imshow(img)


class Image(File):
    """Image loaded with PIL"""

    cached_metadata_fields = File.cached_metadata_fields.copy()
    cached_metadata_fields.update(
        {
            "exif_data": "exif_data",
        }
    )
    initial_data_collection_keys = File.initial_data_collection_keys + ["image", "exif_data"]
    supported_mime_types = ["image/"]

    def __init__(self, path):
        super().__init__(path)
        self.default_viewer = viewers.Image

    def _load_data(self, key):
        """Load image data with PIL"""

        data = super()._load_data(key)
        if data is not None:
            return data

        if key == "image":
            if self.file_info.type == "image/svg+xml":
                return SVGWrapper(self.file_info.path)
            else:
                return PILImage.open(self.file_info.path)

        elif key == "exif_data":
            try:
                return self.get_exif_data()
            except Exception as err:
                return str(err)

    def get_exif_data(self):
        pil_exif = self.image._getexif()
        if pil_exif is None:
            return DataContainer()

        exif = {ExifTags.TAGS[k]: v for k, v in pil_exif.items() if k in ExifTags.TAGS}

        # Convert PIL.TiffImagePlugin.IFDRational to float:
        for k, v in exif.items():
            if isinstance(v, IFDRational):
                exif[k] = float(v)

        return DataContainer(exif)
