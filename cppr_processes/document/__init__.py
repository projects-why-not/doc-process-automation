from .excel import ExcelDocument
from .word import WordDocument


def get_class(doctype):
    if doctype == "Excel":
        return ExcelDocument
    elif doctype == "Word":
        return WordDocument
    else:
        raise ValueError
