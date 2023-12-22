"""
IZD viewer - PySide6 (PyQt6) widget.

Author: Vlad Topan (vtopan/gmail)
"""
import os
import re
import sys
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox, QWidget, \
    QTextBrowser, QStyleFactory, QLabel, QTextEdit, QPushButton, QLineEdit, QCheckBox, \
    QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QClipboard, QKeySequence, QImage, QDesktopServices, \
    QTextDocument, QShortcut

from .libizd import IZDFile
from .libioqt_snap import create_layouts, VLabelEdit


IZDV_CSS_LIGHT = '''
QTextBrowser:!active {
    selection-color: #FFF;
    selection-background-color: #00A;
    }

a {
    text-decoration: none;
}
'''

IZDV_CSS_DARK = '''
* {
    color: #EEC;
    background-color: #111;
    selection-color: #111;
    selection-background-color: #EEA;
}

a:visited {
    color: #DAA;
}

a:hover {
    color: #AA0;
    text-decoration: none;
}

a {
    text-decoration: none;
    color: #FF8;
}

QTextBrowser:!active {
    selection-color: #FFF;
    selection-background-color: #00A;
    }
'''



class VIzdViewer(QWidget):

    def __init__(self, filename=None, dark_mode=False):
        super().__init__()
        self.fieldmap = {}
        self.setMinimumSize(1024, 768)
        widgets = [
            {
                'viewer': Viewer()
            },
            {
                'lbl_find': QLabel('Find (Ctrl+F):'),
                'ed_find': QLineEdit(),
                'b_find': QPushButton('Search (F3)'),
            },
        ]
        self.lay, self.wmap = create_layouts(widgets)
        for k in ('viewer', 'ed_find', 'b_find'):
            setattr(self, k, self.wmap[k])
        self.setLayout(self.lay)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(self.ed_find.setFocus)
        QShortcut(QKeySequence("F5"), self).activated.connect(self.reload)
        QShortcut(QKeySequence("F3"), self).activated.connect(self.find_text)
        QShortcut(QKeySequence("Shift+F3"), self).activated.connect(lambda:self.find_text(back=True))
        self.viewer.anchorClicked.connect(self.link_clicked)
        self.b_find.clicked.connect(self.find_text)
        self.ed_find.returnPressed.connect(self.find_text)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setStyleSheet(IZDV_CSS_DARK if dark_mode else IZDV_CSS_LIGHT)
        self.filename = self.izd = None
        if filename:
            self.open(filename)


    def dbg(self, msg):
        """
        Print a debug message.
        """
        print(msg)


    def err(self, msg, title='ERROR'):
        """
        Pop an error.
        """
        QMessageBox(QMessageBox.Critical, title, msg, QMessageBox.Ok, self).exec()
        self.quit()


    def exc(self, msg):
        """
        Pop an exception (and exit).
        """
        self.dbg(traceback.format_exc())
        self.err(msg, 'CRASHED')


    def open(self, filename):
        """
        Open a document.
        """
        self.filename = filename
        self.izd = IZDFile(filename)
        self.viewer.set_izd(self.izd)


    def reload(self):
        """
        Reload the document.
        """
        sbar = self.viewer.verticalScrollBar()
        pos = sbar.value()
        self.open(self.filename)
        sbar.setValue(pos)


    def link_clicked(self, url):
        """
        Get confirmation before following links.
        """
        if QApplication.keyboardModifiers() == Qt.ControlModifier \
            or QMessageBox(QMessageBox.Question, "Follow external link?",
                f"Open {url.url()} in external browser?\n(Ctrl+click to open directly)",
                QMessageBox.Yes|QMessageBox.No, parent=self).exec() == QMessageBox.Yes:
            QDesktopServices.openUrl(url)


    def find_text(self, back=False):
        """
        Find text changed.
        """
        flags = QTextDocument.FindFlags()
        if back:
            flags |= QTextDocument.FindBackward
        self.viewer.find(self.ed_find.text(), flags)
        self.viewer.setFocus()


    def set_darkmode(self, enable=True):
        """
        Apply/remove dark mode CSS.
        """
        css = [IZDV_CSS_LIGHT, IZDV_CSS_DARK][int(enable)]
        self.setStyleSheet(css)
        self.viewer.document().setDefaultStyleSheet(css)
        self.reload()



class Viewer(QTextBrowser):

    def __init__(self, *args, izd=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setOpenLinks(False)
        self.set_izd(izd)


    def set_izd(self, izd):
        self.izd = izd
        if izd and izd.filename:
            self.setHtml(izd.html)
        else:
            self.clear()


    def loadResource(self, id, url):
        if id == 2:
            # image
            filename = url.path()
            if not re.search(r'^image\d+\.[a-z]{3}$', filename):
                return None
            img = QImage.fromData(self.izd.read_file(filename))
            return img
        else:
            return None

