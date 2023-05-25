from os import sep


class LocalPath:
    def __init__(self, path):
        self._path = path

    def __add__(self, other):
        if self._path[-1] == sep:
            self._path = self._path[:-1]
        return LocalPath(self._path + sep + str(other))

    def __str__(self):
        return self._path
