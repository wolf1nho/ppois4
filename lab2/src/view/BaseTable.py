from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QWidget,
    QTableWidget,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QTableWidgetItem
    )

class BaseTable(QTableWidget):
    def __init__(self):
        super().__init__()
        columns = ["ФИО", "Вид спорта", "Позиция", "Состав", "Титулы", "Разряд"]
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)

        header = self.horizontalHeader()
        header.setStretchLastSection(True)

    def print(self, data):
        self.setRowCount(0)
        for athlete in data:
            row = self.rowCount()
            self.insertRow(row)
            self.setItem(row, 0, QTableWidgetItem(athlete.name))
            self.setItem(row, 1, QTableWidgetItem(athlete.sport))
            self.setItem(row, 2, QTableWidgetItem(athlete.position))
            self.setItem(row, 3, QTableWidgetItem(athlete.team))
            self.setItem(row, 4, QTableWidgetItem(athlete.titles))
            self.setItem(row, 5, QTableWidgetItem(athlete.rank))