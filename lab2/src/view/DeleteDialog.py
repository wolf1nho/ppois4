from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QComboBox,
    QPushButton,
    QGroupBox,
    QLabel
    )

class DeleteAthleteDialog(QDialog):
    def __init__(self, delete_function, parent=None):
        super().__init__(parent)
        self.delete_function = delete_function
        self.deleted_notes = 0
        self.setWindowTitle("Поиск спортсменов")
        #self.setMinimumWidth(500)

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

        self.btn_delete = QPushButton("🔍+🗑️ Удалить")
        self.btn_clear = QPushButton("🧹 Сбросить")
        self.btn_delete.clicked.connect(self.perform)
        self.btn_clear.clicked.connect(self.clear_input)
        search_layout.addRow(self.btn_delete)
        search_layout.addRow(self.btn_clear)

        search_box.setLayout(search_layout)
        layout.addWidget(search_box)

    def get_search_params (self):
        return {
            "name": self.name_input.text().lower(),
            "sport": self.sport_input.text().lower(),
            "rank": self.rank_search.currentText(),
            "min_titles": self.min_titles.value(),
            "max_titles": self.max_titles.value()
        }

    def perform(self):
        self.current_page = 1
        self.deleted_notes = self.delete_function(self.get_search_params())
        self.accept()

    def clear_input(self):
        self.name_input.clear()
        self.sport_input.clear()
        self.min_titles.setValue(0)
        self.max_titles.setValue(100)
        self.rank_search.setCurrentIndex(0)