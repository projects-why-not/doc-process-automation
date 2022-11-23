from .data_item import BasicDataItem
from ...document import get_class


class File(BasicDataItem):
    def __init__(self, path, file_type):
        super().__init__(path)
        self.ftype = file_type
        self._instance = None

    def __call__(self, storage_provider=None):
        if self._instance is None:
            # TODO: download from YaDisk if needed
            self._instance = get_class(self.ftype)(self.path)
        return self._instance


class Template(BasicDataItem):
    def __init__(self, path, file_type):
        super().__init__(path)
        self._type = file_type

    def __call__(self, *args, **kwargs):
        # self._instance = get_class(self._type)(self.path)
        return File(self.storage + "*" + self.path,
                    self._type)
