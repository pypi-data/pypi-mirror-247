"""
Commonly used PySide2 components and wrappers.

Latest version always at: https://gitlab.com/vtopan/libioqt/-/blob/master/libioqt.py

Author: vtopan/gmail
"""
from PySide6.QtWidgets import QLabel, QLineEdit, QLayout, QHBoxLayout, QVBoxLayout, QPushButton, \
    QFrame, QTableView, QHeaderView
from PySide6.QtGui import QKeySequence, QStandardItemModel, QShortcut
from PySide6.QtCore import Qt


VER = '0.1.2.20211229'


def create_layouts(widgets):
    """
    Converts recursive structures of lists, dicts and GUI widgets to a proper PySide2 layout.

    A list is converted to a QVBoxLayout, a dict to a QHBoxLayout, everything else is presumed
    to be a widget and simply added to the current layout. The keys in each dict are mapped to the
    corresponding widgets in the output `widget_map` dict.

    Known keywords:
    - '!vertical' converts a dict to a QVBoxLayout instead of a QHBoxLayout
    - '!horizontal' converts a list to a QHBoxLayout instead of a QVBoxLayout
    - '!border' creates a border (QFrame) around the layout (the value can be CSS styling)
    - '!stretch' sets stretching rules (e.g. '!stretch': (0, 2) sets the stretch property of
        widget 0 to 2

    :return: (top_layout, widget_map)
    """

    def _handle_directive(name, value=None):
        nonlocal res, lay
        if name.startswith('!stretch'):
            lay.setStretch(*value)
        elif name == '!border':
            frame = QFrame()
            res = QHBoxLayout()
            res.addWidget(frame)
            frame.setLayout(lay)
            frame.setFrameStyle(QFrame.StyledPanel)
            if value and isinstance(value, str):
                frame.setStyleSheet(value)
        elif name in ('!horizontal', '!vertical'):
            pass
        else:
            raise ValueError(f'Unknown directive {name}!')

    if not isinstance(widgets, (list, dict)):
        raise ValueError('The toplevel node must be a list or a dict!')
    widget_map = {}
    res = lay = QVBoxLayout() if ((isinstance(widgets, list) and '!horizontal' not in widgets) or '!vertical' in widgets) else QHBoxLayout()
    for e in widgets:
        name = None
        if isinstance(widgets, dict):
            name, e = e, widgets[e]
            if name[0] == '!':
                _handle_directive(name, e)
                continue
        if isinstance(e, (list, dict)):
            e_lay, w_map = create_layouts(e)
            lay.addLayout(e_lay)
            widget_map.update(w_map)
        elif isinstance(e, QLayout):
            lay.addLayout(e)
        elif isinstance(e, str):
            _handle_directive(e)
            continue
        else:
            lay.addWidget(e)
        if name:
            widget_map[name] = e
    return res, widget_map



class VUrlLabel(QLabel):
    """
    URL label.
    """

    def __init__(self, url, title=None):
        super().__init__()
        self.update(url, title)
        self.setOpenExternalLinks(True)


    def update(self, url, title=None):
        self.url = url
        self.title = title or url
        self.setText(f'<a href="{self.url}">{self.title}</a>')


class VTable(QTableView):
    """
    Table wrapper with embedded datamodel.

    :param data: Either a callable (row, column) or a list of lists.
    :param header: A list of (horizontal) header labels.
    """

    def __init__(self, data=None, header=None):
        super().__init__()
        self.dm = QStandardItemModel()
        self.dm.data = self.data
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setModel(self.dm)
        self.setHeader(header)
        if data:
            self.setData(data)
        self.setStyleSheet('QHeaderView::section {border: 1px solid palette(base); background-color: palette(midlight)}')


    def data(self, index, role):
        """
        Datamodel data override.
        """
        row, column = index.row(), index.column()
        if role == Qt.DisplayRole:
            return self._getData(row, column)


    def setHeader(self, labels):
        """
        Set the header labels.
        """
        self._headerLabels = labels


    def setData(self, data):
        """
        Set table data (list of rows).
        """
        self._data = data
        self._getData = self._data if callable(self._data) else \
                lambda row, column: self._data[row][column]
        self.dm.clear()
        if self._headerLabels:
            print(self._headerLabels)
            self.dm.setHorizontalHeaderLabels(self._headerLabels)
        self.dm.setRowCount(len(self._data))
        self.dm.setColumnCount(len(self._data[0]))



def VLabelEdit(label, placeholder='', validator=None, etype=QLineEdit):
    """
    Returns a horizontal layout containing a label and an edit.

    The label and edit widgets are accessible as the `.label` / `.edit` attributes of the layout.
    """
    lay = QHBoxLayout()
    lay.label = QLabel(label)
    lay.addWidget(lay.label)
    lay.edit = etype()
    lay.addWidget(lay.edit)
    lay.label.setBuddy(lay.edit)
    if placeholder:
        lay.edit.setPlaceholderText(placeholder)
    if validator:
        lay.edit.setValidator(validator)
    return lay


def VHBoxLayout(*args, **kwargs):
    lay = QHBoxLayout()
    lay.add(*args, **kwargs)
    return lay


def VVBoxLayout(*args, **kwargs):
    lay = QVBoxLayout()
    lay.add(*args, **kwargs)
    return lay


# monkey-patch sensible methods for layouts
def add_to_layout(self, *things, **kwargs):
    for thing in things:
        if isinstance(thing, QLayout):
            self.addLayout(thing)
        else:
            self.addWidget(thing)
    for name, thing in kwargs.items():
        if isinstance(thing, QLayout):
            self.addLayout(thing)
        else:
            self.addWidget(thing)
        setattr(self, name, thing)


QHBoxLayout.add = add_to_layout
QVBoxLayout.add = add_to_layout


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication, QWidget
    app = QApplication([])
    window = QWidget()
    widgets = [
        {'l1': QLabel('Hello!'), 'b_ok': QPushButton('OK'), 'b_cancel': QPushButton('Cancel')},
        {'l2': QLabel('Enter text #1:'), 'e_1:': QLineEdit('...'), '!border': ''},
        {'le_1': VLabelEdit('Enter text #2:', '...')},
        {'t': VTable([['1', '3', '5'], ('a', 'b', 'z')], ['Col1', 'Col2', 'ColC'])},
        {'b_quit': QPushButton('Quit')},
    ]
    lay, wmap = create_layouts(widgets)
    quit = lambda: app.quit()
    QShortcut(QKeySequence("Esc"), window).activated.connect(quit)
    wmap['b_quit'].clicked.connect(quit)
    window.setLayout(lay)
    window.show()
    app.exec_()
