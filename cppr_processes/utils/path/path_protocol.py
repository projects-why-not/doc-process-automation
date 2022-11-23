

class PathProviderProtocol:
    def __init__(self):
        pass

    def mkdir(self, path):
        raise NotImplementedError

    def rmdir(self, path):
        raise NotImplementedError

    def save(self, path):
        raise NotImplementedError

    def exists(self, path):
        raise NotImplementedError
