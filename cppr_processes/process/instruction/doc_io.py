from tempfile import NamedTemporaryFile

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

    def _perform(self, doc, path, storage_provider=None):
        if type(path) == LocalPath:
            return doc.save(str(path))
        if type(path) == RemotePath:
            virtual_document = NamedTemporaryFile()
            doc.save(virtual_document.name)
            return storage_provider.upload(virtual_document.name, path)
        raise ValueError
