# System library imports
from PyQt4 import QtGui

# Local imports
from syntax_highlighter import PythonHighlighter


class CodeWidget(QtGui.QPlainTextEdit):
    def __init__(self, parent, filename, font=None):
        super(CodeWidget, self).__init__(parent)
        self.set_font(font)
        self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.filename = filename
        self.highlighter = PythonHighlighter(self.document())
        self.is_zoomed = True

    def set_font(self, font):
        if font is None:
            font = QtGui.QFont('Consolas', 11)
        self.document().setDefaultFont(font)

    def color_line(self, line, color):
        selection = QtGui.QTextEdit.ExtraSelection()
        selection.format.setBackground(color)
        selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.movePosition(QtGui.QTextCursor.Start)
        selection.cursor.movePosition(QtGui.QTextCursor.Down,
                                      QtGui.QTextCursor.MoveAnchor,
                                      line-1)

        extraSelections = self.extraSelections()
        if extraSelections is None:
            extraSelections = [selection]
        else:
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def clear_line_coloring(self):
        self.setExtraSelections([])

    def toggle_zoom(self):
        font = self.document().defaultFont()
        if self.is_zoomed:
            font.setPointSize(4)
            self.setFont(font)
        else:
            font.setPointSize(11)
            self.setFont(font)
        self.is_zoomed = not self.is_zoomed


