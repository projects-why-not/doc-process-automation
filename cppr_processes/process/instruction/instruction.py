from xml.etree.ElementTree import Element as XMLTag


class Instruction:
    def __init__(self, subinstructions=None):
        self._subs = subinstructions

    def _perform(self, *args, **kwargs):
        raise NotImplementedError("Must be overridden!")

    # def _perform_xml(self, xml_cmd, data):
    #     raise NotImplementedError("Must be overridden!")

    def __call__(self, *args, **kwargs):
        return self._perform(*args, **kwargs)
        # if type(args[0]) is XMLTag:
        #     if len(args) > 2 or len(kwargs) > 0:
        #         raise Exception("If XML node and data provided, other parameters are restricted!")
        #     return self._perform_xml(*args)
        # else:
        #     return self._perform(*args, **kwargs)
