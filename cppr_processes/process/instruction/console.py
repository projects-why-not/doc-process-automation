from .instruction import Instruction


class Console(Instruction):
    def __init__(self):
        super().__init__()

    def _perform(self, *args):
        print(*args)
