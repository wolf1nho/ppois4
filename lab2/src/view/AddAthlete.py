from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QVBoxLayout)

from PyQt6.QtGui import QIntValidator
from src.view.enums import SPORTS_CONFIG

class AddAthleteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить спортсмена")
        self.setModal(True)

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.name_edit = QLineEdit()
        
        self.sport_combo = QComboBox()
        self.sport_combo.addItems(list(SPORTS_CONFIG.keys()))
        
        self.pos_combo = QComboBox()
        
        self.team_combo = QComboBox()
        self.team_combo.addItems(["основной", "запасной", "n/a"])
        
        self.titles_edit = QLineEdit()
        self.titles_edit.setText("0")
        validator = QIntValidator(0, 1000, self)
        self.titles_edit.setValidator(validator)

        self.rank_combo = QComboBox()
        self.rank_combo.addItems(["1-й юношеский", "2-й разряд", "3-й разряд", "КМС", "Мастер спорта"])

        form_layout.addRow("ФИО:", self.name_edit)
        form_layout.addRow("Вид спорта:", self.sport_combo)
        form_layout.addRow("Позиция:", self.pos_combo)
        form_layout.addRow("Состав:", self.team_combo)
        form_layout.addRow("Титулы:", self.titles_edit)
        form_layout.addRow("Разряд:", self.rank_combo)
        
        layout.addLayout(form_layout)

        self.btn_save = QPushButton("Добавить")
        self.btn_save.clicked.connect(self.accept)
        form_layout.addRow(self.btn_save)
        layout.addWidget(self.btn_save)

        self.sport_combo.currentTextChanged.connect(self.update_dependencies)
        self.update_dependencies()

    def update_dependencies(self):
        sport = self.sport_combo.currentText()

        # Получаем настройки для выбранного спорта (пустой конфиг по умолчанию)
        config = SPORTS_CONFIG.get(sport, {"positions": ["n/a"], "is_team": False})

        # 1. Обновляем комбобокс позиций
        self.pos_combo.clear()
        self.pos_combo.addItems(config["positions"])

        # 2. Логика управления полем состава (Team/Solo)
        is_team_sport = config["is_team"]

        if not is_team_sport:
            # Если спорт одиночный
            self.team_combo.setCurrentText("n/a")
            self.team_combo.setEnabled(False)
            self.pos_combo.setEnabled(False)
        else:
            # Если спорт командный
            self.team_combo.setEnabled(True)
            self.pos_combo.setEnabled(True)
            # Если до этого стояло "n/a", сбрасываем на первый доступный вариант (например, "Основной")
            if self.team_combo.currentText() == "n/a":
                self.team_combo.setCurrentIndex(0)

    def get_data(self):
        return {
            "name": self.name_edit.text(),
            "sport": self.sport_combo.currentText(),
            "position": self.pos_combo.currentText(),
            "team": self.team_combo.currentText(),
            "titles": self.titles_edit.text(),
            "rank": self.rank_combo.currentText()
        }