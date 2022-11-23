from ..document_block import DocumentBlock


class WordDocumentTextBlock(DocumentBlock):
    def __init__(self, instance, name):
        super().__init__(instance, name)
        self._text = instance.text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._instance.text = value


class WordDocumentTableField(DocumentBlock):
    def __init__(self, instance, name):
        super().__init__(instance, name)
        self._text = instance.text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._instance.text = value


class WordDocumentTable(DocumentBlock):
    def __init__(self, instance, name, subblocks):
        super().__init__(instance, name, subblocks)
