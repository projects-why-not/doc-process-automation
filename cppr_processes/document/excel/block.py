from openpyxl.cell import MergedCell

from ..document_block import DocumentBlock


def next_letter(let):
    if len(let) == 0:
        return "A"
    if let[-1] == "Z":
        return next_letter(let[:-1]) + "A"
    return let[:-1] + chr(ord(let[-1]) + 1)


class ExcelRow(DocumentBlock):
    def __init__(self, instance, name, cells):
        super().__init__(instance, name, cells)

    def __set__(self, value):
        raise Exception("Cannot set a value to the Row! Specify the field instead")

    def add_cell(self, cell, title):
        self._blocks[title] = cell

    def remove_cell(self, title):
        del self._blocks[title]


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
    def __init__(self, instance, name, rows, headers):
        super().__init__(instance, name, rows)
        self._headers = headers

    def __set__(self, value):
        raise Exception("Cannot set a value to the Sheet! Specify the field instead")

    def clear_row(self, row_ind):
        for letter, title in self._headers.items():
            cell = self._instance[f"{letter}{row_ind + 2}"]
            if type(cell) is not MergedCell:
                cell.value = ''

    def insert_row(self):
        row_ind = len(self._blocks) + 2

        cells = {}
        for letter, title in self._headers.items():
            cells[title] = ExcelCell(self._instance[f"{letter}{row_ind}"], f"{letter}{row_ind}")

        row = ExcelRow(None, row_ind - 2, cells)
        self.clear_row(row_ind)
        self._blocks[str(row_ind - 2)] = row

    def remove_row(self):
        self.clear_row(len(self._blocks) - 1)
        del self._blocks[str(len(self._blocks) - 1)]

    def get_last_column_letter(self):
        last_letter = 'A'
        for letter in self._headers.keys():
            if len(letter) > len(last_letter) or letter > last_letter:
                last_letter = letter
        return last_letter

    def clear_column(self, column_letter):
        title_cell = self._instance[f"{column_letter}1"]
        if type(title_cell) is not MergedCell:
            title_cell.value = ''

        for idx, row in self._blocks.items():
            cell = self._instance[f"{column_letter}{int(idx) + 2}"]
            if type(cell) is not MergedCell:
                cell.value = ''

    def insert_column(self, title):
        new_letter = next_letter(self.get_last_column_letter())

        self._headers[new_letter] = title
        for idx, row in self._blocks.items():
            cell = ExcelCell(self._instance[f"{new_letter}{int(idx) + 2}"], f"{new_letter}{int(idx) + 2}")
            row.add_cell(cell, title)

        self.clear_column(new_letter)
        title_cell = self._instance[f"{new_letter}1"]
        if type(title_cell) is not MergedCell:
            title_cell.value = title

    def remove_column(self):
        last_letter = self.get_last_column_letter()

        self.clear_column(last_letter)

        title = self._headers[last_letter]
        del self._headers[last_letter]
        for row in self._blocks.values():
            row.remove_cell(title)
