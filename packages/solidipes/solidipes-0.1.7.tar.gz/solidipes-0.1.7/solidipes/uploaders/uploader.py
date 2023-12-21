from abc import ABC, abstractmethod


class Uploader(ABC):
    command = None
    command_help = None

    @abstractmethod
    def upload(self, args):
        pass

    @abstractmethod
    def populate_arg_parser(self, parser):
        pass
