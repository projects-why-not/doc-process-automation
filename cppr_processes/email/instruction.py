from cppr_processes.email.backend import EMailBackend
from cppr_processes.process.instruction.instruction import Instruction
from tempfile import NamedTemporaryFile


class EMailInstruction(Instruction):
    def __init__(self):
        super().__init__()

    def _perform(self, backend, subject, body, files, receivers, cc, bcc):
        virtual_files = []
        for filename, doc in files:
            virtual_document = NamedTemporaryFile()
            doc.save(virtual_document.name)
            virtual_files.append((filename, virtual_document))
        backend.send(receivers, subject, body, virtual_files, cc, bcc)
