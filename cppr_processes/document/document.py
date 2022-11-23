from ..utils.path import LocalPath
from os import sep


class Document:
    def __init__(self, path):
        self._path = str(LocalPath(path))
        self._f_instance = self.open()
        self._fields = self._parse_fields()

    def _parse_fields(self):
        raise NotImplementedError("Must be overridden in subclass!")

    def __getitem__(self, item):
        if item == "name":
            return self._path.split(sep)[-1]
        return self._fields[item]

    def __iter__(self):
        if self._fields is None:
            raise StopIteration

        self._iter_ind = -1
        return self

    def __next__(self):
        self._iter_ind += 1
        if self._iter_ind >= len(self._fields):
            raise StopIteration
        return list(self._fields.values())[self._iter_ind]

    def open(self):
        raise NotImplementedError("Must be overridden in subclass!")

    def save(self, path):
        raise NotImplementedError("Must be overridden in subclass!")
