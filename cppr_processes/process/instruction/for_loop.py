from .instruction import Instruction


class For(Instruction):
    def __init__(self, subinstructions):
        super().__init__(subinstructions)

    def _perform(self, elems):
        try:
            for subelem in elems:
                for instr in self._subs:
                    instr.perform(subelem)
        except:
            return False
        return True
