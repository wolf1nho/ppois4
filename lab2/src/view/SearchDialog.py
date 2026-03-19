from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QGroupBox,
    QLabel,
    QMessageBox
    )
from PyQt6.QtCore import Qt
from src.view.BaseTable import BaseTable
from src.view.PaginationPanel import PaginationPanel
from src.controller.Paginator import Paginator
from src.view.EditDialog import EditAthleteDialog

class SearchDialog(QDialog):
    def __init__(self, search_function, delete_function, parent=None):
        super().__init__(parent)
        self.search_function = search_function
        self.delete_function = delete_function
        self.setWindowTitle("Поиск спортсменов")
        self.resize(900, 700)

        layout = QVBoxLayout(self)

        search_box = QGroupBox("Критерии поиска")
        search_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.sport_input = QLineEdit()
        
        titles_layout = QHBoxLayout()
        self.min_titles = QSpinBox()
        self.max_titles = QSpinBox()
        self.max_titles.setRange(0, 999)
        self.max_titles.setValue(100)
        titles_layout.addWidget(QLabel("Титулов от:"))
        titles_layout.addWidget(self.min_titles)
        titles_layout.addWidget(QLabel("до:"))
        titles_layout.addWidget(self.max_titles)

        self.rank_search = QComboBox()
        self.rank_search.addItems(["Любой", "1-й юношеский", "2-й разряд", "3-й разряд", "КМС", "Мастер спорта"])

        search_layout.addRow("ФИО:", self.name_input)
        search_layout.addRow("Вид спорта:", self.sport_input)
        search_layout.addRow("Диапазон титулов:", titles_layout)
        search_layout.addRow("Разряд:", self.rank_search)

        self.btn_find = QPushButton("🔍 Найти")
        self.btn_clear = QPushButton("🧹 Сбросить")
        self.btn_delete_selected = QPushButton("🗑️ Удалить выбранного")
        self.btn_edit = QPushButton("✏️ Редактировать")
        self.btn_find.clicked.connect(self.perform_search)
        self.btn_clear.clicked.connect(self.clear_input)
        self.btn_delete_selected.clicked.connect(self.handle_delete_selected)
        self.btn_edit.clicked.connect(self.handle_edit)
        search_layout.addRow(self.btn_find)
        search_layout.addRow(self.btn_clear)
        search_layout.addRow(self.btn_delete_selected)
        search_layout.addRow(self.btn_edit)

        search_box.setLayout(search_layout)
        layout.addWidget(search_box)

        self.table = BaseTable()
        layout.addWidget(self.table)

        self.pagination_panel = PaginationPanel()
        layout.addLayout(self.pagination_panel)

        self.paginator = Paginator(self.table, self.pagination_panel)

        self.perform_search()

    def get_search_params (self):
        return {
            "name": self.name_input.text().lower(),
            "sport": self.sport_input.text().lower(),
            "rank": self.rank_search.currentText(),
            "min_titles": self.min_titles.value(),
            "max_titles": self.max_titles.value()
        }

    def perform_search(self):
        self.current_page = 1
        self.paginator.set_data(self.search_function(self.get_search_params()))

    def update_table(self):
        self.perform_search()

    def handle_delete_selected(self):
        row_in_table = self.table.currentRow()
        if row_in_table < 0:
            QMessageBox.warning(self, "Внимание", "Выберите спортсмена для удаления!")
            return

        page_size = self.pagination_panel.get_page_size()

        athlete = self.paginator.get_athlete(self.paginator.current_page, page_size, row_in_table)

        ans = QMessageBox.question(self, "Подтверждение", 
                                 f"Удалить спортсмена {athlete.name} из базы?",
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if ans == QMessageBox.StandardButton.Yes:
            self.delete_function(athlete)
            
            self.update_table()
            
            QMessageBox.information(self, "Успех", "Запись удалена из базы.")

    def handle_edit(self):
        row_in_table = self.table.currentRow()
        if row_in_table < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования!")
            return

        page_size = self.pagination_panel.get_page_size()

        athlete = self.paginator.get_athlete(self.paginator.current_page, page_size, row_in_table)

        dialog = EditAthleteDialog(self)
        dialog.set_data(athlete)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()

            athlete.name = new_data["name"]
            athlete.sport = new_data["sport"]
            athlete.position = new_data["position"]
            athlete.team = new_data["team"]
            athlete.titles = new_data["titles"]
            athlete.rank = new_data["rank"]

            self.update_table()
            QMessageBox.information(self, "Успех", "Данные обновлены!")

    def clear_input(self):
        self.name_input.clear()
        self.sport_input.clear()
        self.min_titles.setValue(0)
        self.max_titles.setValue(100)
        self.rank_search.setCurrentIndex(0)
        self.perform_search()