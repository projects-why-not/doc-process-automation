from datetime import datetime

from .instruction import Instruction
from ...document.document_block import DocumentBlock
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
            if isinstance(res.text, datetime):
                if res.text.hour == 0 and res.text.minute == 0 and res.text.second == 0:
                    return res.text.date()
            return res.text
        return str(res)


class Set(Instruction):
    def __init__(self):
        super().__init__()

    def _perform(self, elem, key, value, *text_filters):
        value = str(value)
        for filt in text_filters:
            if type(filt) is str:
                filt_f = getattr(StringUtils, filt)
                filt_params = {}
            else:
                filt_f = getattr(StringUtils, filt[0])
                filt_params = filt[1]
            value = filt_f(value, *filt_params)

        pts = key.split("@")
        tgt = elem[pts[0]]
        has_placeholder = False
        for i in range(1, len(pts)):
            has_subblocks = getattr(tgt, "has_subblocks", None)
            if callable(has_subblocks) and not has_subblocks():
                tgt.text = tgt.text.replace(pts[i], value)
                has_placeholder = True
            else:
                tgt = tgt[pts[i]]

        if not has_placeholder:
            tgt.text = value
        return True