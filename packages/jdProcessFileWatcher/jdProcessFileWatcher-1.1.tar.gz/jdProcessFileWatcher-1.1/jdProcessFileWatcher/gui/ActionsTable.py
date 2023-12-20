from ..Functions import clear_table_widget, stretch_table_widget_colum_size, format_time
from ..ui_compiled.ActionsTable import Ui_ActionsTable
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from ..core.Filter import PathFilter, FilterList
from .FilterWidgets import BasicFilterWidgets
from ..FileAction import FileAction
from ..Types import FileChangedData
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..Environment import Environment


class _TableColumns:
    ACTION = 0
    PATH = 1
    TIME = 2
    PID = 3
    ProcessName = 4


class ActionsTable(QWidget, Ui_ActionsTable):
    def __init__(self, env: "Environment", autoscroll: bool) -> None:
        super().__init__()

        self.setupUi(self)

        self._env = env
        self._autoscroll = autoscroll
        self._data_list: list[FileChangedData] = []

        self._current_fitler = FilterList()

        stretch_table_widget_colum_size(self.main_table)

        self._basic_filter_widgets = BasicFilterWidgets()
        self.main_layout.addWidget(self._basic_filter_widgets)

        self.path_filter_edit.textChanged.connect(self._update_filter_list)
        self._basic_filter_widgets.filter_changed.connect(self._update_filter_list)

    def _update_filter_list(self) -> None:
        self._current_filter = FilterList()
        self._basic_filter_widgets.fill_filter_list(self._current_filter)

        if self.path_filter_edit.text() != "":
            self._current_filter.append(PathFilter(self.path_filter_edit.text().strip()))

        for row, data in enumerate(self._data_list):
            if self._current_filter.check_data(data):
                self.main_table.showRow(row)
            else:
                self.main_table.hideRow(row)

    def add_data(self, data: FileChangedData) -> None:
        row = self.main_table.rowCount()

        self.main_table.insertRow(row)

        self.main_table.setItem(row, _TableColumns.ACTION, QTableWidgetItem(FileAction.get_display_name(data.action)))
        self.main_table.setItem(row, _TableColumns.TIME, QTableWidgetItem(format_time(data.time, self._env.settings.get("timeFormat"))))
        self.main_table.setItem(row, _TableColumns.PATH, QTableWidgetItem(data.path))
        self.main_table.setItem(row, _TableColumns.PID, QTableWidgetItem(str(data.pid)))
        self.main_table.setItem(row, _TableColumns.ProcessName, QTableWidgetItem(str(data.process_name)))

        self._data_list.append(data)

        self._basic_filter_widgets.add_data(data)

        if not self._current_filter.check_data(data):
            self.main_table.hideRow(row)

        if self._autoscroll:
            self.main_table.scrollToBottom()

    def clear(self) -> None:
        self._data_list.clear()
        clear_table_widget(self.main_table)
        self._basic_filter_widgets.reset()
        self.path_filter_edit.setText("")
        self._current_filter = FilterList()
