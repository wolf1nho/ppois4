from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QPushButton
    )
from src.view.BaseTable import BaseTable
from src.view.PaginationPanel import PaginationPanel
from PyQt6.QtGui import QAction
from src.controller.AthleteController import AthleteController
from src.controller.Paginator import Paginator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Учет спортсменов")
        self.setGeometry(200, 100, 900, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

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
        self.main_layout.addLayout(btn_layout)

        self.table = BaseTable()

        self.main_layout.addWidget(self.table)

        self.pagination_panel = PaginationPanel()

        self.main_layout.addLayout(self.pagination_panel)

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

        self.action_exit.triggered.connect(self.close)

        edit_menu = menu_bar.addMenu("&Записи")

        self.action_add = QAction("Добавить", self)
        self.action_search = QAction("Поиск", self)
        self.action_delete = QAction("Удалить", self)

        edit_menu.addAction(self.action_add)
        edit_menu.addAction(self.action_search)
        edit_menu.addAction(self.action_delete)
    
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

    def connect_buttons(self, controller: AthleteController):
        self.btn_add.clicked.connect(controller.handle_add)
        self.btn_edit.clicked.connect(controller.handle_edit)
        self.btn_search.clicked.connect(controller.handle_search)
        self.btn_delete_selected.clicked.connect(controller.handle_delete_selected)
        self.btn_delete.clicked.connect(controller.handle_delete)

        self.action_add.triggered.connect(controller.handle_add)
        self.action_search.triggered.connect(controller.handle_search)
        self.action_delete.triggered.connect(controller.handle_delete)

        self.action_open.triggered.connect(controller.handle_import)
        self.action_save.triggered.connect(controller.handle_export)
        
    def get_selected_row(self) -> int:
        return self.table.currentRow()
    
    def get_page_size(self) -> int:
        return self.pagination_panel.get_page_size()