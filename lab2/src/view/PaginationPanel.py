from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QWidget,
    QTableWidget,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QSpinBox
    )

class PaginationPanel(QHBoxLayout):
    def __init__(self):
        super().__init__()
        
        self.btn_first = QPushButton("« Первая")
        self.btn_prev = QPushButton("‹")
        self.page_info = QLabel("Страница 1/1 (Всего: 0)")
        self.btn_next = QPushButton("›")
        self.btn_last = QPushButton("Последняя »")
        self.btn_prev.setEnabled(False)
        self.btn_first.setEnabled(False)
        self.btn_next.setEnabled(False)
        self.btn_last.setEnabled(False)
        
        self.page_size = QSpinBox()
        self.page_size.setRange(1, 100)
        self.page_size.setValue(10)

        self.addWidget(self.btn_first)
        self.addWidget(self.btn_prev)
        self.addStretch()
        self.addWidget(self.page_info)
        self.addStretch()
        self.addWidget(self.btn_next)
        self.addWidget(self.btn_last)
        self.addWidget(QLabel("Показывать по:"))
        self.addWidget(self.page_size)

    def connect_buttons(self, paginator):
        self.btn_first.clicked.connect(paginator.go_first)
        self.btn_prev.clicked.connect(paginator.go_prev)
        self.btn_next.clicked.connect(paginator.go_next)
        self.btn_last.clicked.connect(paginator.go_last)
        self.page_size.valueChanged.connect(paginator.change_page_size)

    def update(self, current_page, total_pages, total_notes):
        self.page_info.setText(f"Страница {current_page}/{total_pages} (Всего: {total_notes})")
        
    def get_page_size(self):
        return self.page_size.value()
