from ..document_block import DocumentBlock


class ExcelRow(DocumentBlock):
    def __init__(self, instance, name, cells):
        super().__init__(instance, name, cells)

    def __set__(self, value):
        raise Exception("Cannot set a value to the Row! Specify the field instead")


class ExcelCell(DocumentBlock):
    def __init__(self, instance, name):
        super().__init__(instance, name)
        self._text = instance.value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._instance.value = value


class ExcelSheet(DocumentBlock):
    def __init__(self, instance, name, rows):
        super().__init__(instance, name, rows)

    def __set__(self, value):
        raise Exception("Cannot set a value to the Sheet! Specify the field instead")
