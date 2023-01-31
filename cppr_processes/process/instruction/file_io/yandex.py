from ..instruction import Instruction
from ....utils.yandex_disk_provider import YandexDiskProvider


class YandexDiskInstruction(Instruction):
    server = None

    def __init__(self, server=None):
        super().__init__()
        self.server = server

    def _perform(self, *args):
        if args[0] == "login":
            self.server = YandexDiskProvider().login(*args[1:])
            return self.server
        if self.server is None:
            raise Exception("Ya Disk is not initialized!")

        return getattr(self.server, args[0])(*args[1:])
