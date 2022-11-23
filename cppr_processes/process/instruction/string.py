from .instruction import Instruction
from ...utils.string import StringUtils


class FormattedString(Instruction):
    def __init__(self):
        super().__init__()

    def _perform(self, *args, **kwargs):
        fmt_str = args[0]
        output = fmt_str.format(*args[1:])

        if "filter" in kwargs and kwargs["filter"] is not None:
            for filt in kwargs["filter"]:
                if type(filt) is str:
                    filt_f = getattr(StringUtils, filt)
                    filt_params = {}
                else:
                    filt_f = getattr(StringUtils, filt[0])
                    filt_params = filt[1]
                output = filt_f(output, **filt_params)

        return output
