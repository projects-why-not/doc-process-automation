from .instruction import Instruction
from ...utils.path import *
from ...document import get_class


class OpenDocument(Instruction):
    def __init__(self):
        super().__init__()

    def _perform(self, path, doctype):
        return get_class(doctype)(path)


class SaveDocument(Instruction):
    def __init__(self):
        super().__init__()

    def _perform(self, doc, path):
        return doc.save(str(LocalPath(path)))
