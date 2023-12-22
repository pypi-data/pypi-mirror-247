#!/usr/bin/env python3
"""
PySide6-based viewer for IZD files.

Author: Vlad Topan (vtopan/gmail)
"""
import json
import os
import re
import sys
import traceback

from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QWidget, \
    QTextBrowser, QStyleFactory, QLabel, QTextEdit, QPushButton, QLineEdit, QCheckBox, \
    QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QClipboard, QIcon, QKeySequence, QImage, QDesktopServices, \
    QTextDocument, QShortcut

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))
from libizd import VIzdViewer, IZDV_CSS_LIGHT, IZDV_CSS_DARK
from libizd.libioqt_snap import create_layouts, VLabelEdit


__VER__ = '1.0.1'

APP_PATH = os.path.dirname(__file__)
CFG_FILE = f'{APP_PATH}/vizd-config.json'
CFG = {'dark_mode': False, 'ui':{}}



class MainWindow(QMainWindow):

    def __init__(self, app, filename=None):
        global MAINWINDOW
        super().__init__()
        MAINWINDOW = self
        self.setWindowTitle('IZD Viewer')
        self.clipboard = QApplication.clipboard()
        self.app = app
        self.setWindowIcon(QIcon(f'{APP_PATH}/vizd.png'))
        self.create_ui_elements()
        self.setCentralWidget(self.main)
        QShortcut(QKeySequence("Esc"), self).activated.connect(self.quit)
        QShortcut(QKeySequence("Alt+Left"), self).activated.connect(self.viewer.viewer.backward)
        QShortcut(QKeySequence("Ctrl+O"), self).activated.connect(self.open_clicked)
        self.cb_dark.edit.stateChanged.connect(self.darkmode_toggled)
        self.setFocusPolicy(Qt.StrongFocus)
        if os.path.isfile(CFG_FILE):
            self.load_config()
        self.setStyleSheet(IZDV_CSS_DARK if CFG['dark_mode'] else IZDV_CSS_LIGHT)
        if filename:
            self.viewer.open(filename)


    def load_config(self):
        """
        Load & apply configuration.
        """
        CFG.update(json.load(open(CFG_FILE)))
        if 'pos' in CFG['ui']:
            self.move(*CFG['ui']['pos'])
        if 'size' in CFG['ui']:
            self.resize(*CFG['ui']['size'])
        if CFG['ui'].get('maximized', False):
            self.showMaximized()
        if CFG['dark_mode']:
            self.cb_dark.edit.setChecked(True)


    def save_config(self):
        """
        Save configuration.
        """
        CFG['ui'] = {}
        CFG['ui']['pos'] = self.pos().toTuple()
        CFG['ui']['size'] = self.size().toTuple()
        CFG['ui']['maximized'] = self.isMaximized()
        json.dump(CFG, open(CFG_FILE, 'w'))


    def create_ui_elements(self):
        self.fieldmap = {}
        self.main = QWidget()
        widgets = [
            {
                '_': QLabel('Options:'),
                'cb_dark': VLabelEdit('Dark mode', etype=QCheckBox),
            },
            {
                'viewer': VIzdViewer()
            },
        ]
        self.lay, self.wmap = create_layouts(widgets)
        for k in ('cb_dark', 'viewer'):
            setattr(self, k, self.wmap[k])
        self.cb_dark.edit.setTristate(False)
        self.main.setLayout(self.lay)


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


    def exc(self, msg):
        """
        Pop an exception (and exit).
        """
        self.dbg(traceback.format_exc())
        self.err(msg, 'CRASHED')
        self.quit()


    def quit(self):
        """
        Close app.
        """
        self.save_config()
        self.app.quit()


    def open_clicked(self):
        """
        Browse for a file to open.
        """
        filename, _ = QFileDialog.getOpenFileName(None, "Open IZD document", "",
                "All Files (*);;IZD Documents (*.izd);;ZIP Files (*.zip)",
                "IZD Documents (*.izd)")
        if filename:
            self.viewer.open(filename)


    def darkmode_toggled(self):
        """
        Apply/remove dark mode CSS.
        """
        CFG['dark_mode'] = self.cb_dark.edit.isChecked()
        self.save_config()
        self.viewer.set_darkmode(CFG['dark_mode'])



def run(args=sys.argv):
    app = QApplication(args)
    app.setStyle(QStyleFactory.create("Plastique"))
    filename = None if len(sys.argv) < 2 else sys.argv[1]
    main = MainWindow(app, filename)
    main.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    try:
        sys.exit(run(sys.argv))
    except Exception as e:
        sys.stderr.write(f'[!] Dead: {e}\n')
        raise
