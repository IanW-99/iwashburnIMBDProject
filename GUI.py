import sqlite3

from PyQt5.QtWidgets import QMainWindow, QPushButton
import api_interaction


class MainWindow(QMainWindow):

    def __init__(self, conn: sqlite3.Connection, curs: sqlite3.Cursor):
        self.conn = conn
        self.curs = curs
        super().__init__()

        self.update_data_button = QPushButton(self)
        self.data_visualization_menu_button = QPushButton(self)

        self.data_visualization = DataVisualization(self, self.conn, self.curs)

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('iwashburnIMDBProject')
        self.setGeometry(400, 200, 1000, 750)
        self.setFixedSize(1000, 750)

        self.update_data_button.setText("Update Data")
        self.update_data_button.resize(150, 50)
        self.update_data_button.move(50, 200)
        self.update_data_button.clicked.connect(self.update_data)

        self.data_visualization_menu_button.setText("Data Visualization")
        self.data_visualization_menu_button.resize(150, 50)
        self.data_visualization_menu_button.move(50, 250)
        self.data_visualization_menu_button.clicked.connect(self.open_data_visualization)

    def open_data_visualization(self):
        self.hide()
        self.DataVisualization.show()

    def update_data(self):
        api_interaction.data_grab_and_store(self.conn, self.curs)


class DataVisualization(QMainWindow):

    def __init__(self, previous_window, conn: sqlite3.Connection, curs: sqlite3.Cursor):
        self.conn = conn
        self.curs = curs
        self.previous_window = previous_window
        super(DataVisualization, self).__init__()
        self.setWindowTitle('iwashburnIMDBProject/DataVisualization')
        self.setGeometry(400, 200, 1000, 750)
        self.setFixedSize(1000, 750)
