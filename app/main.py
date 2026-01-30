# main.py
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
import db  # Import your db.py logic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget(self)
        self.setCentralWidget(self.table)
        self.load_data()

    def load_data(self):
        # Call the helper function from db.py
        data = db.fetch_data("SELECT * FROM users;")
        
        if data:
            self.table.setRowCount(len(data))
            self.table.setColumnCount(len(data[0]))
            for row_idx, row_data in enumerate(data):
                for col_idx, value in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
