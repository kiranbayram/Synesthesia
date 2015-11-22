# Standard library imports
import sys

# System library imports
from PyQt4 import QtGui

# Local imports
from main_window import MainWindow

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())