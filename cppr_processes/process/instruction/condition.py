from .instruction import Instruction
import numpy as np


class IfCondition(Instruction):
    comp_ops = {"eq": lambda x, y: x == y,
                "l": lambda x, y: x < y,
                "leq": lambda x, y: x <= y,
                "g": lambda x, y: x > y,
                "geq": lambda x, y: x >= y,
                "neq": lambda x, y: x != y}
    logical_ops = {"&": lambda x: sum(x) == len(x),
                   "|": lambda x: sum(x) >= 1,
                   "-": lambda x: sum(x) == 0}

    def __init__(self):
        super().__init__()

    def _perform(self, cmd_info, *operands):
        kind = cmd_info["kind"]
        if kind in ["eq", "g", "geq", "l", "leq", "neq"]:
            return self._perform_comparison(kind, operands)
        elif kind in ["&", "|", "-"]:
            return self._perform_logical(kind, operands)
        else:
            raise ValueError(f"Unknown kind of condition - {kind}!")

    def _perform_comparison(self, kind, operands):
        if len(operands) != 2:
            raise ValueError(f"Exactly two operands must be provided for {kind} condition!")
        return self.comp_ops[kind](*operands)

    def _perform_logical(self, kind, operands):
        for op in operands:
            if op not in [True, False]:
                raise ValueError(f"Only logical T or F are allowed inside {kind} condition!")
        return self.logical_ops[kind](np.array(operands).astype(int))
