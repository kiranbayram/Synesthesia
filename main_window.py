# Standard library imports
import sys
import os
import imp

# System library imports
from PyQt4 import QtGui
from PyQt4 import QtCore

# Local imports
from statistical_analyser import StatisticalAnalyser
from code_editor_widget import CodeWidget
from color_gradient import *
from tab_widget import TabWidget
from util import get_func_names, get_list_names


class MainWindow(QtGui.QMainWindow):

    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    WINDOW_TITLE = 'Synesthesia'
    CODE_EDITOR_FONT = QtGui.QFont('Consolas', 11)

    def __init__(self):
        super(MainWindow, self).__init__();
        self._init_icons()
        self._init_window_properties()
        self._init_actions()
        self._init_widgets()
        self._init_menubar()
        self._init_toolbar()
        self._init_layout()

    def _init_window_properties(self):
        self.setGeometry(50, 50, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setWindowIcon(self.icon_python)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.statusBar()

    def _init_icons(self):
        self.icon_open = QtGui.QIcon('images/open_22.png')
        self.icon_save = QtGui.QIcon('images/save_22.png')
        self.icon_run_analysis = QtGui.QIcon('images/run_analysis_22.png')
        self.icon_clear_coverage = QtGui.QIcon('images/clear_22.png')
        self.icon_refresh = QtGui.QIcon('images/refresh_22.png')
        self.icon_zoom = QtGui.QIcon('images/zoom_22.png')
        self.icon_python = QtGui.QIcon('images/python-icon.svg')

    def _init_actions(self):
        self.action_exit = QtGui.QAction('Exit', self)
        self.action_exit.setStatusTip('Exit application')
        self.action_exit.triggered.connect(QtGui.qApp.quit)

        self.action_open_file = QtGui.QAction(self.icon_open, 'Open File...', self)
        self.action_open_file.setStatusTip('Open Python source file')
        self.action_open_file.triggered.connect(self.open_file)

        self.action_save_file = QtGui.QAction(self.icon_save, 'Save File', self)
        self.action_save_file.setStatusTip('Save changes to the File')
        self.action_save_file.setShortcut('Ctrl+S')
        self.action_save_file.triggered.connect(self.save_file)

        self.action_run_analysis = QtGui.QAction(self.icon_run_analysis, 'Run Analysis', self)
        self.action_run_analysis.setStatusTip('Run statistical analysis')
        self.action_run_analysis.triggered.connect(self.run_analysis)

        self.action_clear_coverage = QtGui.QAction(self.icon_clear_coverage, 'Clear Coverage', self)
        self.action_clear_coverage.setStatusTip('Clear the colored coverage')
        self.action_clear_coverage.triggered.connect(self.clear_coverage)

        self.action_show_about_dialog = QtGui.QAction('About Synesthesia', self)
        self.action_show_about_dialog.triggered.connect(self.show_about_dialog)

        self.action_refresh_definitions = QtGui.QAction(self.icon_refresh, 'Reload Definitions', self)
        self.action_refresh_definitions.setStatusTip('Reload method and input lists definitions of currently opened file')
        self.action_refresh_definitions.triggered.connect(self.load_definitions)

        self.action_toggle_zoom = QtGui.QAction(self.icon_zoom, 'Toggle Zoom / Dezoom', self)
        self.action_toggle_zoom.setStatusTip('Toggle between zoomed and dezoomed view.')
        self.action_toggle_zoom.triggered.connect(self.toggle_zoom)

    def _init_widgets(self):
        self.tab_editor_widget = TabWidget(self)
        self.code_editors_widgets = []

    def _init_menubar(self):
        file_menu = self.menuBar().addMenu('File')
        file_menu.addAction(self.action_open_file)
        file_menu.addAction(self.action_save_file)
        file_menu.addAction(self.action_exit)

        debug_menu = self.menuBar().addMenu('Debug')
        debug_menu.addAction(self.action_run_analysis)
        debug_menu.addAction(self.action_clear_coverage)
        debug_menu.addAction(self.action_refresh_definitions)
        debug_menu.addAction(self.action_toggle_zoom)

        help_menu = self.menuBar().addMenu('Help')
        help_menu.addAction(self.action_show_about_dialog)

    def _init_toolbar(self):
        self.toolbar = self.addToolBar('Shortcuts')
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)
        self.toolbar.addAction(self.action_open_file)
        self.toolbar.addAction(self.action_save_file)
        self.toolbar.addAction(self.action_run_analysis)
        self.toolbar.addAction(self.action_clear_coverage)
        self.toolbar.addAction(self.action_refresh_definitions)
        self.toolbar.addAction(self.action_toggle_zoom)

    def _init_layout(self):
        layout = QtGui.QGridLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(self.tab_editor_widget, 1, 0, 1, 4)
        self.right_widget = QtGui.QWidget()
        rightLayout = QtGui.QVBoxLayout()
        self.module_label = QtGui.QLabel()
        self.func_combobox = QtGui.QComboBox()
        self.testFunc_combobox = QtGui.QComboBox()
        self.input_combobox = QtGui.QComboBox()
        self.passed_input_label = QtGui.QLabel()
        self.failed_input_label = QtGui.QLabel()
        self.result_label = QtGui.QLabel("Results:")
        self.result_label.setVisible(False)
        rightLayout.addWidget(QtGui.QLabel('Module:'))
        rightLayout.addWidget(self.module_label)
        rightLayout.addWidget(QtGui.QLabel('Function to be analyzed:'))
        rightLayout.addWidget(self.func_combobox)
        rightLayout.addWidget(QtGui.QLabel('Test Function:'))
        rightLayout.addWidget(self.testFunc_combobox)
        rightLayout.addWidget(QtGui.QLabel('Input List:'))
        rightLayout.addWidget(self.input_combobox)
        rightLayout.addWidget(self.result_label)
        rightLayout.addWidget(self.passed_input_label)
        rightLayout.addWidget(self.failed_input_label)
        rightLayout.addStretch(2)
        self.right_widget.setLayout(rightLayout)
        layout.addWidget(self.right_widget,1,4)
        central_widget = QtGui.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_file(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self, caption='Open file',
                                                      filter='Python files (*.py);;All files (*)')
        if file_name != '':
            self.load_file(unicode(file_name.toUtf8(), encoding="utf-8"))

    def load_file(self, file_name):
        # Clear all opened files.
        self.code_editors_widgets = []
        self.tab_editor_widget.remove_all_tabs()

        # Create new code editor in new tab
        code_editor = CodeWidget(self, file_name, self.CODE_EDITOR_FONT)
        self.code_editors_widgets.append(code_editor)
        self.tab_editor_widget.add_new_tab(code_editor)

        # Load file in new code editor
        file_ = open(file_name, 'r')
        code_editor.setPlainText(file_.read())
        file_.close()

        # Load method and input list definition
        self.load_definitions()

    def load_definitions(self):
        # Stop if no file is currently open
        if self.tab_editor_widget.currentWidget() is None:
            return
        # Clear all combo boxes
        self.func_combobox.clear()
        self.testFunc_combobox.clear()
        self.input_combobox.clear()

        # Find all method and lists in the opened file.
        module_name = self.tab_editor_widget.currentWidget().filename
        sys.path.append(os.path.dirname(module_name))
        buggy_module = imp.load_source(os.path.basename(module_name)[:-3], module_name)
        name_list = dir(buggy_module)
        func_names = get_func_names(buggy_module, name_list)
        list_names = get_list_names(buggy_module, name_list)
        sys.path.pop()

        # Set the current module to the current tab
        self.module_name = module_name
        self.module_label.setText('-> ' + os.path.basename(module_name))
        
        self.result_label.setVisible(False)
        self.passed_input_label.setText("")
        self.failed_input_label.setText("")

        # Add the found method / list names to the combo boxes
        self.func_combobox.addItems(func_names)
        self.testFunc_combobox.addItems(func_names)
        self.input_combobox.addItems(list_names)

    def save_file(self):
        code_editor = self.tab_editor_widget.currentWidget()
        if code_editor is None:
            return
        file_ = open(code_editor.filename, 'w')
        file_.write(code_editor.toPlainText())
        file_.close()
        code_editor.document().setModified(False)

    def run_analysis(self):
        # The following hack forces Python to reload all opened modules
        for code_editor in self.code_editors_widgets:
            module_name = os.path.basename(code_editor.filename)[:-3]
            imp.load_source(module_name, code_editor.filename)

        if self.tab_editor_widget.currentWidget() is not None:
            analyser = StatisticalAnalyser()
            module_name = self.module_name
            method_name = str(self.func_combobox.currentText())
            test_name = str(self.testFunc_combobox.currentText())
            inputs_name = str(self.input_combobox.currentText())
            analyser.statistical_debug(module_name, method_name, test_name, inputs_name)
            if analyser.isTestFuncCorrect:
                successes, fails = analyser.get_input_statistics()
                self.result_label.setVisible(True)
                self.passed_input_label.setText("Number of Passed Inputs: "+str(successes))
                self.failed_input_label.setText("Number of Failed Inputs: "+str(fails))
                line_phi = analyser.get_line_phi()
                self.display_coverage(line_phi)
            else:
                QtGui.QMessageBox.warning(self, 'Warning', 'Please provide a correct test function!', QtGui.QMessageBox.Ok)
            
        else:
            QtGui.QMessageBox.warning(self, 'Warning', 'No code to analyze. Please load a python file!', QtGui.QMessageBox.Ok)

    def display_coverage(self, coverage):
        self.clear_coverage()
        for filename in coverage:
            if self.tab_editor_widget.get_widget(filename) is None:
                code_editor = CodeWidget(self, filename, self.CODE_EDITOR_FONT)
                self.code_editors_widgets.append(code_editor)
                file_ = open(filename, 'r')
                code_editor.setPlainText(file_.read())
                file_.close()
                code_editor.show()
                self.tab_editor_widget.add_new_tab(code_editor)
            else:
                code_editor = self.tab_editor_widget.get_widget(filename)

            for line in coverage[filename]:
                phi = coverage[filename][line]
                if not phi == 'NaN':
                    code_editor.color_line(line, green_red_percentile(phi * 50 + 50))
                else:
                    code_editor.color_line(line, QtGui.QColor(200, 200, 200, 127))

    def clear_coverage(self):
        for code_editor in self.code_editors_widgets:
            code_editor.clear_line_coloring()

    def toggle_zoom(self):
        current_editor = self.tab_editor_widget.currentWidget()
        if current_editor is not None:
            current_editor.toggle_zoom()

    def show_about_dialog(self):
        about_text = 'Synesthesia\nPython statistical debugger\n\nNisa Bozkurt\nBayram Kiran\nKevin Salvesen'
        QtGui.QMessageBox.about(self, 'About Synesthesia', about_text)
