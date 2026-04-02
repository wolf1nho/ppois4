import sys
from PyQt6.QtWidgets import QApplication
from src.view.MainWindow import MainWindow
from src.controller.AthleteController import AthleteController
from src.model.AthleteModel import AthleteModel

def main():
    app = QApplication(sys.argv)

    model = AthleteModel()

    window = MainWindow()

    controller = AthleteController(model, window)

    controller.view = window

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()