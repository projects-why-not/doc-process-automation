from os import sep


class LocalPath:
    def __init__(self, path):
        self._path = path

    def __add__(self, other):
        return LocalPath(self._path + sep + str(other))

    def __str__(self):
        return self._path
