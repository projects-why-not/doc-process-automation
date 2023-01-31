import os

from .data_item import BasicDataItem
from ..instruction import YandexDiskInstruction
from ...document import get_class, get_default_extension


class File(BasicDataItem):
    def __init__(self, path, file_type):
        super().__init__(path)
        self.ftype = file_type
        self._instance = None

    def __call__(self, storage_provider=None):
        if self._instance is None:
            if storage_provider is None:
                self._instance = get_class(self.ftype)(self.path)
            else:
                temp_file_name = "__temp" + get_default_extension(self.ftype)
                YandexDiskInstruction(storage_provider)("download", self.path, temp_file_name)
                self._instance = get_class(self.ftype)(temp_file_name)
                os.remove(temp_file_name)
        return self._instance


class Template(BasicDataItem):
    def __init__(self, path, file_type):
        super().__init__(path)
        self._type = file_type

    def __call__(self, *args, **kwargs):
        # self._instance = get_class(self._type)(self.path)
        return File(self.storage + "*" + self.path,
                    self._type)
