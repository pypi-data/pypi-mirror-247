import argparse
import importlib
import inspect
import pkgutil

import solidipes.uploaders
from solidipes.uploaders.uploader import Uploader

command = "upload"
command_help = "Upload dataset to an online repository"


def get_uploaders():
    module_names = [
        module.name
        for module in pkgutil.iter_modules(solidipes.uploaders.__path__)
        if module.name != "uploader"  # Skip the base abstract class
    ]

    modules = [importlib.import_module(f"solidipes.uploaders.{module_name}") for module_name in module_names]

    uploaders = [get_uploader_subclass(module)() for module in modules]

    return {uploader.command: uploader for uploader in uploaders}


def get_uploader_subclass(module):
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, Uploader) and obj != Uploader:
            return obj

    raise NotImplementedError(f"Could not find subclass of Uploader in module {module}")


uploaders = get_uploaders()


def main(args):
    platform = args.platform
    uploader_module = uploaders[platform]
    uploader_module.upload(args)


def populate_arg_parser(parser):
    # Create subparsers for each upload platform
    uploader_parsers = parser.add_subparsers(dest="platform", help="Target hosting platform")
    uploader_parsers.required = True

    for uploader in uploaders.values():
        uploader_parser = uploader_parsers.add_parser(uploader.command, help=uploader.command_help)
        uploader.populate_arg_parser(uploader_parser)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    populate_arg_parser(parser)
    args = parser.parse_args()
    main(args)
