from cppr_processes.email.backend import EMailBackend
from cppr_processes.process.instruction.instruction import Instruction
from tempfile import NamedTemporaryFile


class EMailInstruction(Instruction):
    def __init__(self):
        super().__init__()

    def _perform(self, doc, backend, subject, body, filename, receivers):
        virtual_document = NamedTemporaryFile()
        doc.save(virtual_document.name)
        backend.send(receivers, subject, body, [(filename, virtual_document)])
