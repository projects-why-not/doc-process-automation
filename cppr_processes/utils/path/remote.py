from urllib.parse import unquote


class RemotePath:
    def __init__(self, path):
        self._path = unquote(path)

    def __add__(self, other):
        return RemotePath(self._path + "/" + other)

    def __str__(self):
        return self._path
