from src.view.AddAthlete import AddAthleteDialog

class EditAthleteDialog(AddAthleteDialog):
    def set_data(self, athlete):
        self.setWindowTitle("Редактировать запись")
        self.btn_save.setText("Сохранить")
        self.name_edit.setText(athlete.name)
        self.sport_combo.setCurrentText(athlete.sport)
        self.pos_combo.setCurrentText(athlete.position)
        self.team_combo.setCurrentText(athlete.team)
        self.titles_edit.setText(athlete.titles)
        self.rank_combo.setCurrentText(athlete.rank)
