from PyQt6.QtWidgets import QMainWindow, QLabel, QTreeWidgetItem, QInputDialog, QMessageBox, QFileDialog, QHeaderView, QApplication, QMenu
from ..Types import FileChangedData, StartProcessInfo
from ..ui_compiled.MainWindow import Ui_MainWindow
from .PathActionsDialog import PathActionsDialog
from typing import cast, Optional, TYPE_CHECKING
from .RunCommandDialog import RunCommandDialog
from .RunProgramDialog import RunProgramDialog
from .FilterWidgets import BasicFilterWidgets
from PyQt6.QtCore import Qt, QCoreApplication, QPoint
from ..Functions import is_process_running
from .SettingsDialog import SettingsDialog
from ..StraceWrapper import StraceWrapper
from .WelcomeDialog import WelcomeDialog
from .ActionsTable import ActionsTable
from ..core.Filter import FilterList
from .AboutDialog import AboutDialog
from PyQt6.QtGui import QAction, QCursor
import webbrowser
import subprocess
import pathlib
import copy
import html
import sys
import os


if TYPE_CHECKING:
    from ..Environment import Environment


class _FileTreeColumns:
    NAME = 0
    OWN_COUNT = 1
    RECUSRIVE_COUNT = 2


class FileTreeItem(QTreeWidgetItem):
    def __init__(self, main_window: "MainWindow", parent: Optional["FileTreeItem"], name: str, path: str) -> None:
        super().__init__(parent)

        self._parent_widget = parent
        self._main_window = main_window
        self._data_list: list[FileChangedData] = []

        self.path = path
        self.is_directory: bool = False

        self.setText(_FileTreeColumns.NAME, name)
        self.setText(_FileTreeColumns.OWN_COUNT, "0")
        self.setText(_FileTreeColumns.RECUSRIVE_COUNT, "0")

    def get_child_list(self) -> list["FileTreeItem"]:
        item_list: list["FileTreeItem"] = []

        for i in range(self.childCount()):
            item_list.append(self.child(i))

        return item_list

    def get_child_by_name(self, name: str) -> Optional["FileTreeItem"]:
        for child in self.get_child_list():
            if child.text(0) == name:
                return child

        return None

    def update_item(self) -> None:
        own_count = len(self._main_window.current_file_tree_filter.filter_list(self._data_list))
        self.setText(_FileTreeColumns.OWN_COUNT, str(own_count))

        recursive_count = len(self._main_window.current_file_tree_filter.filter_list(self.get_recursive_data()))
        self.setText(_FileTreeColumns.RECUSRIVE_COUNT, str(recursive_count))
        self.setHidden(recursive_count == 0)

        self.is_directory = recursive_count > own_count

    def update_item_tree(self) -> None:
        self.update_item()

        if self._parent_widget is not None:
            self._parent_widget.update_item_tree()

    def update_item_recursive(self) -> None:
        self.update_item()

        for child in self.get_child_list():
            child.update_item_recursive()

    def add_data(self, data: FileChangedData) -> None:
        self._data_list.append(data)

        self.update_item_tree()

    def get_own_data(self) -> list[FileChangedData]:
        return copy.copy(self._data_list)

    def get_recursive_data(self) -> list[FileChangedData]:
        data_list = self.get_own_data()

        for child in self.get_child_list():
            data_list += child.get_recursive_data()

        return data_list

    def get_context_menu(self) -> QMenu:
        menu = QMenu()

        show_actions_action = QAction(QCoreApplication.translate("FileTreeItem", "Show Actions"), self._main_window)
        show_actions_action.triggered.connect(lambda: self._main_window.path_actions_dialog.open_dialog(self))
        menu.addAction(show_actions_action)

        menu.addSeparator()

        copy_path_action = QAction(QCoreApplication.translate("FileTreeItem", "Copy Path"), self._main_window)
        copy_path_action.triggered.connect(lambda: QApplication.clipboard().setText(self.path))
        menu.addAction(copy_path_action)

        copy_name_action = QAction(QCoreApplication.translate("FileTreeItem", "Copy Name"), self._main_window)
        copy_name_action.triggered.connect(lambda: QApplication.clipboard().setText(os.path.basename(self.path)))
        menu.addAction(copy_name_action)

        if self._parent_widget is not None:
            copy_directory_action = QAction(QCoreApplication.translate("FileTreeItem", "Copy Directory Path"), self._main_window)
            copy_directory_action.triggered.connect(lambda: QApplication.clipboard().setText(os.path.dirname(self.path)))
            menu.addAction(copy_directory_action)

        menu.addSeparator()

        open_file_action = QAction(QCoreApplication.translate("FileTreeItem", "Open"), self._main_window)
        open_file_action.triggered.connect(lambda: subprocess.Popen(["xdg-open", self.path]))
        menu.addAction(open_file_action)

        if not self.is_directory and self._parent_widget is not None:
            open_directory_action = QAction(QCoreApplication.translate("FileTreeItem", "Open Directory"), self._main_window)
            open_directory_action.triggered.connect(lambda: subprocess.Popen(["xdg-open", os.path.dirname(self.path)]))
            menu.addAction(open_directory_action)

        return menu


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, env: "Environment") -> None:
        super().__init__()

        self.setupUi(self)

        self._process_running_label = QLabel()
        self.statusBar().addPermanentWidget(self._process_running_label)

        self._actions_table = ActionsTable(env, True)
        self.actions_table_layout.addWidget(self._actions_table)

        self.path_actions_dialog = PathActionsDialog(env, self)
        self._run_command_dialog = RunCommandDialog(self)
        self._run_program_dialog = RunProgramDialog(self, env.icon)
        self._settings_dialog = SettingsDialog(env, self)
        self.welcome_dialog = WelcomeDialog(env, self)
        self._about_dialog = AboutDialog(env, self)

        self._strace_wrapper = StraceWrapper(env)
        self._strace_wrapper.file_changed.connect(self._file_changed)
        self._strace_wrapper.process_started.connect(self._process_started)
        self._strace_wrapper.process_finished.connect(self._process_stoped)
        self.current_file_tree_filter = FilterList()

        self.file_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.file_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.file_tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        self._file_tree_root_item = FileTreeItem(self, None, "/", "/")
        self.file_tree.addTopLevelItem(self._file_tree_root_item)

        self._file_tree_filter_widgets = BasicFilterWidgets()
        self.file_tree_layout.addWidget(self._file_tree_filter_widgets)
        self._file_tree_filter_widgets.filter_changed.connect(self._file_tree_filter_changed)
        self.file_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.file_tree.itemDoubleClicked.connect(self._file_tree_item_double_clicked)
        self.file_tree.customContextMenuRequested.connect(self._file_tree_context_menu)

        self.run_command_action.triggered.connect(self._run_command_dialog.open_dialog)
        self.run_program_action.triggered.connect(self._run_program_dialog.open_dialog)
        self.attach_process_action.triggered.connect(self._attach_process_clicked)
        self.load_strace_log_action.triggered.connect(self._load_strace_log_clicked)
        self.exit_action.triggered.connect(lambda: sys.exit(0))

        self.terminate_process_action.triggered.connect(self._strace_wrapper.terminate_process)
        self.kill_process_action.triggered.connect(self._strace_wrapper.kill_process)

        self.settings_action.triggered.connect(self._settings_dialog.open_dialog)

        self.show_welcome_dialog_action.triggered.connect(self.welcome_dialog.open_dialog)
        self.view_source_action.triggered.connect(lambda: webbrowser.open("https://codeberg.org/JakobDev/jdProcessFileWatcher"))
        self.report_bug_action.triggered.connect(lambda: webbrowser.open("https://codeberg.org/JakobDev/jdProcessFileWatcher/issues"))
        self.translate_action.triggered.connect(lambda: webbrowser.open("https://translate.codeberg.org/projects/jdProcessFileWatcher"))
        self.donate_action.triggered.connect(lambda: webbrowser.open("https://ko-fi.com/jakobdev"))
        self.about_action.triggered.connect(self._about_dialog.open_dialog)
        self.about_qt_action.triggered.connect(QApplication.instance().aboutQt)

        self.tab_widget.tabBar().setDocumentMode(True)
        self.tab_widget.tabBar().setExpanding(True)

        self.tab_widget.setCurrentIndex(0)

        self._process_stoped()

    def _file_tree_item_double_clicked(self, item: FileTreeItem) -> None:
        self.path_actions_dialog.open_dialog(item)

    def _file_tree_context_menu(self, pos: QPoint) -> None:
        item = cast(FileTreeItem, self.file_tree.itemAt(pos))

        if item is None:
            return

        item.get_context_menu().exec(QCursor.pos())

    def _add_to_file_tree(self, data: FileChangedData) -> None:
        current_item = self._file_tree_root_item

        for part in pathlib.Path(data.path).parts[1:]:
            item = current_item.get_child_by_name(part)
            if item is not None:
                current_item = item
            else:
                item = FileTreeItem(self, current_item, part, os.path.join(current_item.path, part))
                current_item = item

        current_item.add_data(data)

    def _file_changed(self, data: FileChangedData) -> None:
        self._actions_table.add_data(data)
        self._add_to_file_tree(data)
        self._file_tree_filter_widgets.add_data(data)

    def _file_tree_filter_changed(self, filter_list: FilterList) -> None:
        self.current_file_tree_filter = filter_list
        self._file_tree_root_item.update_item_recursive()

    def _attach_process_clicked(self) -> None:
        pid, ok = QInputDialog.getInt(self, QCoreApplication.translate("MainWindow", "Attach Process"), QCoreApplication.translate("MainWindow", "Please enter the PID of the Process"), min=1)

        if not ok:
            return

        if not is_process_running(pid):
            QMessageBox.critical(self, QCoreApplication.translate("MainWindow", "Process not found"), QCoreApplication.translate("MainWindow", "There is no process with the PID {{pid}}").replace("{{pid}}", str(pid)))
            return

        self.clear()
        self._strace_wrapper.attach_process(pid)

    def _load_strace_log_clicked(self) -> None:
        text = QCoreApplication.translate("MainWindow", "This function allows you to load an existing strace log instead of monitoring a running process.") + " "
        text += QCoreApplication.translate("MainWindow", "The logfile must be generated using the following command:") + "<br><br>"
        text += subprocess.list2cmdline(["strace"] + self._strace_wrapper.get_strace_arguments()) + " " + html.escape(QCoreApplication.translate("MainWindow", "<command>")) + " 2> " + html.escape(QCoreApplication.translate("MainWindow", "<path>"))

        match QMessageBox.warning(self, QCoreApplication.translate("MainWindow", "Load strace log"), text, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel):
            case QMessageBox.StandardButton.Ok:
                pass
            case QMessageBox.StandardButton.Cancel:
                return

        path = QFileDialog.getOpenFileName(self, directory=os.path.expanduser("~"))[0]

        if path == "":
            return

        self.clear()

        try:
            self._strace_wrapper.load_log_file(path)
        except Exception:
            QMessageBox.critical(self, QCoreApplication.translate("MainWindow", "Error"), QCoreApplication.translate("MainWindow", "{{path}} could not be parsed. Please ensure it has the correct format.").replace("{{path}}", path))

    def _process_started(self, pid: int) -> None:
        self._process_running_label.setText(QCoreApplication.translate("MainWindow", "Process {{pid}} is currently running").replace("{{pid}}", str(pid)))

        self.terminate_process_action.setEnabled(True)
        self.kill_process_action.setEnabled(True)

    def _process_stoped(self) -> None:
        self._process_running_label.setText(QCoreApplication.translate("MainWindow", "No process is running"))

        self.terminate_process_action.setEnabled(False)
        self.kill_process_action.setEnabled(False)

    def clear(self) -> None:
        self._actions_table.clear()

        self.file_tree.clear()
        self._file_tree_root_item = FileTreeItem(self, None, "/", "/")
        self.file_tree.addTopLevelItem(self._file_tree_root_item)

        self._file_tree_filter_widgets.reset()

    def start_process(self, info: StartProcessInfo) -> None:
        self.clear()
        self._strace_wrapper.start_process(info)
