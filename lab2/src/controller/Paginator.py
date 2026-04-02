from src.view.BaseTable import BaseTable
from src.view.PaginationPanel import PaginationPanel
from src.model.Athlete import Athlete

class Paginator:
    def __init__(self, table: BaseTable, pagination: PaginationPanel):
        self.data = []
        self.table: BaseTable = table
        self.current_page = 1
        self.pagination: PaginationPanel = pagination
        pagination.connect_buttons(self)

    def set_data(self, new_data):
        self.data = new_data
        self.current_page = 1

    def get_current_page(self):
        return self.current_page

    def update_table(self):
        total_count = len(self.data)
        page_size = self.pagination.get_page_size()

        total_pages = max(1, (total_count + page_size - 1) // page_size)
        self.pagination.update(self.current_page, total_pages, len(self.data))

        self.pagination.btn_prev.setEnabled(self.current_page > 1)
        self.pagination.btn_first.setEnabled(self.current_page > 1)
        self.pagination.btn_next.setEnabled(self.current_page < total_pages)
        self.pagination.btn_last.setEnabled(self.current_page < total_pages)

        start = page_size * (self.current_page - 1)

        self.table.print(self.data[start:start + page_size])

    def get_athlete(self, current_page, page_size, row_in_table) -> Athlete:
        return self.data[(current_page - 1 ) * page_size + row_in_table]

    def go_first(self):
        self.current_page = 1
        self.update_table()

    def go_last(self):
        total_count = len(self.data)
        page_size = self.pagination.get_page_size()
        total_pages = max(1, (total_count + page_size - 1) // page_size)
        self.current_page = total_pages
        self.update_table()

    def go_next(self):
        self.current_page += 1
        self.update_table()

    def go_prev(self):
        self.current_page -= 1
        self.update_table()

    def change_page_size(self):
        self.current_page = 1
        self.update_table()