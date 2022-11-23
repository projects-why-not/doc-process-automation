

class DocumentBlock:
    def __init__(self, instance, name, subblocks=None):
        self._instance = instance
        self._name = name
        self._blocks = subblocks
        self._iter_ind = None

    def __getitem__(self, item):
        if item == "name":
            return self._name
        return self._blocks[item]

    def __iter__(self):
        if self._blocks is None:
            raise StopIteration

        self._iter_ind = -1
        return self

    def __next__(self):
        self._iter_ind += 1
        if self._iter_ind >= len(self._blocks):
            raise StopIteration
        return list(self._blocks.values())[self._iter_ind]
