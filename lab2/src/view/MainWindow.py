from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QWidget,
    QTableWidget,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QDialog,
    QMessageBox,
    QFileDialog
    )
from src.view.BaseTable import BaseTable
from src.view.PaginationPanel import PaginationPanel
from PyQt6.QtGui import QAction
from src.controller.AthleteController import AthleteController
from src.controller.Paginator import Paginator
from src.view.AddAthlete import AddAthleteDialog
from src.view.EditDialog import EditAthleteDialog
from src.model.Athlete import Athlete
from src.view.SearchDialog import SearchDialog
from src.view.DeleteDialog import DeleteAthleteDialog

class MainWindow(QMainWindow):
    def __init__(self, controller: AthleteController):
        super().__init__()
        self.controller = controller
        self.controller.view = self
        
        self.setWindowTitle("Учет спортсменов")
        self.setGeometry(200, 100, 900, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("➕ Добавить спортсмена")
        self.btn_edit = QPushButton("✏️ Редактировать")
        self.btn_search = QPushButton("🔍 Найти")
        self.btn_delete_selected = QPushButton("🗑️ Удалить выбранного")
        self.btn_delete = QPushButton("🔍+🗑️ Удалить")
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_search)
        btn_layout.addWidget(self.btn_delete_selected)
        btn_layout.addWidget(self.btn_delete)
        self.layout.addLayout(btn_layout)

        self.btn_add.clicked.connect(self.handle_add)
        self.btn_edit.clicked.connect(self.handle_edit)
        self.btn_search.clicked.connect(self.handle_search)
        self.btn_delete_selected.clicked.connect(self.handle_delete_selected)
        self.btn_delete.clicked.connect(self.handle_delete)
        self.table = BaseTable()

        self.layout.addWidget(self.table)

        self.pagination_panel = PaginationPanel()

        self.layout.addLayout(self.pagination_panel)

        self.paginator = Paginator(self.table, self.pagination_panel)

        self.create_menu_bar()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&Файл")
        
        self.action_open = QAction("Открыть", self)
        self.action_save = QAction("Сохранить", self)
        self.action_exit = QAction("Выход", self)
        
        file_menu.addAction(self.action_open)
        file_menu.addAction(self.action_save)
        file_menu.addSeparator()
        file_menu.addAction(self.action_exit)

        self.action_open.triggered.connect(self.handle_import)
        self.action_save.triggered.connect(self.handle_export)
        self.action_exit.triggered.connect(self.close)

        edit_menu = menu_bar.addMenu("&Записи")

        self.action_add = QAction("Добавить", self)
        self.action_search = QAction("Поиск", self)
        self.action_delete = QAction("Удалить", self)

        edit_menu.addAction(self.action_add)
        edit_menu.addAction(self.action_search)
        edit_menu.addAction(self.action_delete)

        self.action_add.triggered.connect(self.handle_add)
        self.action_search.triggered.connect(self.handle_search)
        self.action_delete.triggered.connect(self.handle_delete)
    
    def create_buttons(self):
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("➕ Добавить спортсмена")
        self.btn_edit = QPushButton("✏️ Редактировать")
        self.btn_search = QPushButton("🔍 Найти")
        self.btn_delete_selected = QPushButton("🗑️ Удалить выбранного")
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_search)
        btn_layout.addWidget(self.btn_delete_selected)

    def connect_buttons(self, controller):
        self.btn_add.clicked.connect(self.handle_add)
        self.btn_edit.clicked.connect(controller.handle_edit)
        self.btn_delete_selected.clicked.connect(controller.handle_delete)
        self.btn_search.clicked.connect(controller.handle_search)

    def update_table(self):
        self.paginator.set_data(self.controller.notes)

    def handle_add(self):
        dialog = AddAthleteDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            
            if not data["name"].strip():
                QMessageBox.warning(self, "Ошибка", "ФИО не может быть пустым!")
                return
            if not data["titles"].strip():
                QMessageBox.warning(self, "Ошибка", "Количество титулов не может быть пустым!")
                return

            new_athlete = Athlete(
                data["name"], data["sport"], data["position"],
                data["team"], data["titles"], data["rank"]
            )
        
            self.controller.add(new_athlete)
            self.update_table()

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
            #QMessageBox.information(self, "Успех", "Данные обновлены!")

    def handle_search(self):
        dialog = SearchDialog(self.controller.search, self.controller.delete, self)
        dialog.exec()
        self.update_table()

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
            self.controller.delete(athlete)
            
            self.update_table()
            
            QMessageBox.information(self, "Успех", "Запись удалена из базы.")

    def handle_delete(self):
        dialog = DeleteAthleteDialog(self.controller.delete_searched, self)
        deleted_notes = dialog.exec()
        self.update_table()
        if deleted_notes > 0:
            QMessageBox.information(self, "Результат", f"Удалено записей: {deleted_notes}")
        else:
            QMessageBox.warning(self, "Результат", "Записей по данным условиям не найдено.")

    def handle_import(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Загрузить данные", "", "XML Files (*.xml)")
        if file_path:
            try:
                self.controller.handle_import(file_path)
                self.update_table()
                QMessageBox.information(self, "Успех", f"Загружено {len(self.controller.notes)} записей.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось прочитать файл:\n{str(e)}")

    def handle_export(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить данные", "", "XML Files (*.xml)")
        if file_path:
            try:
                self.controller.handle_export(file_path)
                QMessageBox.information(self, "Успех", "Данные успешно сохранены.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
        
    def get_selected_row(self):
        return self.table.currentRow()