import sys
from PyQt6.QtWidgets import QApplication
from src.view.MainWindow import MainWindow
from src.controller.AthleteController import AthleteController

def main():
    app = QApplication(sys.argv)

    controller = AthleteController()

    window = MainWindow(controller)

    controller.view = window

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()