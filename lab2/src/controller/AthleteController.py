from src.model.Athlete import Athlete
from src.model.AthleteModel import AthleteModel
from src.view.AddAthlete import AddAthleteDialog
from src.view.EditDialog import EditAthleteDialog
from src.model.Athlete import Athlete
from src.view.SearchDialog import SearchDialog
from src.view.DeleteDialog import DeleteAthleteDialog
from PyQt6.QtWidgets import (
    QDialog,
    QMessageBox,
    QFileDialog
    )
from src.controller.Paginator import Paginator

class AthleteController:
    def __init__(self, model = None, view = None):
        self.view = view
        self.view.controller = self
        self.paginator: Paginator = view.paginator
        self.model: AthleteModel = model
        self.view.connect_buttons(self)

    def handle_add(self):
        dialog = AddAthleteDialog(self.view)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            
            if not data["name"].strip():
                QMessageBox.warning(self.view, "Ошибка", "ФИО не может быть пустым!")
                return
            if not data["titles"].strip():
                QMessageBox.warning(self.view, "Ошибка", "Количество титулов не может быть пустым!")
                return

            new_athlete = Athlete(
                data["name"], data["sport"], data["position"],
                data["team"], data["titles"], data["rank"]
            )
        
            self.model.add(new_athlete)
            self.paginator.set_data(self.model.get_data())
            self.paginator.update_table()

    def handle_edit(self):
        row_in_table = self.view.get_selected_row()
        if row_in_table < 0:
            QMessageBox.warning(self.view, "Ошибка", "Выберите запись для редактирования!")
            return

        page_size = self.view.get_page_size()

        athlete = self.paginator.get_athlete(self.paginator.get_current_page(), page_size, row_in_table)

        dialog = EditAthleteDialog(self.view)
        dialog.set_data(athlete)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()

            athlete.name = new_data["name"]
            athlete.sport = new_data["sport"]
            athlete.position = new_data["position"]
            athlete.team = new_data["team"]
            athlete.titles = new_data["titles"]
            athlete.rank = new_data["rank"]

            self.paginator.update_table()

    def handle_search(self):
        dialog = SearchDialog(self.model.search, self.model.delete, self.view)
        dialog.exec()
        self.paginator.update_table()

    def handle_delete_selected(self):
        row_in_table = self.view.get_selected_row()
        if row_in_table < 0:
            QMessageBox.warning(self.view, "Внимание", "Выберите спортсмена для удаления!")
            return

        page_size = self.view.get_page_size()

        athlete = self.paginator.get_athlete(self.paginator.current_page, page_size, row_in_table)

        ans = QMessageBox.question(self.view, "Подтверждение", 
                                 f"Удалить спортсмена {athlete.name} из базы?",
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if ans == QMessageBox.StandardButton.Yes:
            self.model.delete(athlete)
            
            self.paginator.update_table()
            
            QMessageBox.information(self.view, "Успех", "Запись удалена из базы.")

    def handle_delete(self):
        dialog = DeleteAthleteDialog(self.model.delete_searched, self.view)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if dialog.deleted_notes > 0:
                self.paginator.update_table()
                QMessageBox.information(self.view, "Результат", f"Удалено записей: {dialog.deleted_notes}")
            else:
                QMessageBox.warning(self.view, "Результат", "Записей по данным условиям не найдено.")
        

    def handle_import(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Загрузить данные", "", "XML Files (*.xml)")
        if file_path:
            try:
                self.model.handle_import(file_path)
                self.paginator.set_data(self.model.get_data())
                self.paginator.update_table()
                QMessageBox.information(self.view, "Успех", f"Загружено {len(self.model.get_data())} записей.")
            except Exception as e:
                QMessageBox.critical(self.view, "Ошибка", f"Не удалось прочитать файл:\n{str(e)}")

    def handle_export(self):
        file_path, _ = QFileDialog.getSaveFileName(self.view, "Сохранить данные", "", "XML Files (*.xml)")
        if file_path:
            try:
                self.model.handle_export(file_path)
                QMessageBox.information(self.view, "Успех", "Данные успешно сохранены.")
            except Exception as e:
                QMessageBox.critical(self.view, "Ошибка", f"Не удалось сохранить файл:\n{str(e)}")