from .instruction import Instruction
from ...utils.string import StringUtils


class Get(Instruction):
    def __init__(self):
        super().__init__()

    def _perform(self, elem, key):
        pts = key.split("@")
        res = elem[pts[0]]
        for i in range(1, len(pts)):
            res = res[pts[i]]
        if type(res) is str:
            return res
        if hasattr(res, "text"):
            return res.text
        return str(res)


class Set(Instruction):
    def __init__(self):
        super().__init__()

    def _perform(self, elem, key, value, *text_filters):
        pts = key.split("@")
        tgt = elem[pts[0]]
        for i in range(1, len(pts)):
            tgt = tgt[pts[i]]

        value = str(value)
        for filt in text_filters:
            if type(filt) is str:
                filt_f = getattr(StringUtils, filt)
                filt_params = {}
            else:
                filt_f = getattr(StringUtils, filt[0])
                filt_params = filt[1]
            value = filt_f(value, *filt_params)

        tgt.text = value
        return True