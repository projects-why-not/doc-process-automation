from os import sep


class BasicDataItem:
    def __init__(self, path):
        self.storage = path.split("*")[0]
        self.path = "*".join(path.split("*")[1:])
        self._instance = None
        self.name = path  # .split(sep)[:-1]

    def __call__(self, *args, **kwargs):
        return self._instance

    def __getitem__(self, item):
        if item == "name":
            return self.name
        raise AttributeError
