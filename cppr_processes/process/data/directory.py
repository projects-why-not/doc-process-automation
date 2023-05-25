from ...utils.path import LocalPath, RemotePath
from ..instruction import YandexDiskInstruction
from .data_item import BasicDataItem
from .file import File
from os import listdir, sep


class Directory(BasicDataItem):
    def __init__(self, path):
        super().__init__(path)
        self.kind, self._instance = path.split("*")[0], "*".join(path.split("*")[1:])
        self.server = None
        if self.kind not in ["local", "yadisk"]:
            raise ValueError("Wrong directory type!")

    @classmethod
    def _parse_f_type(cls, path):
        ext = path.split(sep)[-1].split(".")[-1]
        if ext in ["xls", "xlsx"]:
            return "Excel"
        elif ext in ["doc", "docx"]:
            return "Word"
        else:
            return None

    def _list(self):
        if self.kind == "local":
            files = listdir(self._instance)
            format_path = lambda x: str(LocalPath(self._instance) + x)
        else:
            files = YandexDiskInstruction(self.server)("list", self._instance)
            format_path = lambda x: str(RemotePath(x))
        return [format_path(f) for f in files]

    def __iter__(self):
        self._iter_values = self._list()
        self._i = -1
        return self

    def __next__(self):
        self._i += 1
        if self._i >= len(self._iter_values):
            raise StopIteration
        fpath = self._iter_values[self._i]
        return File(fpath,
                    self._parse_f_type(fpath))
