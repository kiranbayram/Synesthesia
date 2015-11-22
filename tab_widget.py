# Standard library imports
import os

# System library imports
from PyQt4.QtGui import QTabWidget, QTextEdit


class TabWidget(QTabWidget):
    def __init__(self, parent):
        super (TabWidget, self).__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.setMovable(True)

    def add_new_tab(self, codeEditor):
        codeEditor.modificationChanged.connect(self.update_tab_name)
        self.addTab(codeEditor, os.path.basename(codeEditor.filename))

    def close_tab(self, index):
        self.last_closed_editor =  self.widget(index)
        self.removeTab(index)

    def remove_all_tabs(self):
        for i in range(self.count()):
            self.removeTab(0)

    def get_widget(self, fname):
        for i in range(self.count()):
            if self.widget(i).filename == fname:
                return self.widget(i)
        return None

    def update_tab_name(self, is_modified):
        tab_title = os.path.basename(self.currentWidget().filename)
        if is_modified:
            tab_title = tab_title + '*'
        self.setTabText(self.currentIndex(), tab_title)
