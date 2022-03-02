import sqlite3

from PyQt5.QtWidgets import QMainWindow, QPushButton, QTableWidget, QTableWidgetItem
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
        self.data_visualization.show()

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

        self.tv_data_open = False
        self.tv_data = QPushButton(self)
        self.movie_data_open = False
        self.movie_data = QPushButton(self)

        self.tv_data.setText('Tv Data')
        self.tv_data.resize(150, 50)
        self.tv_data.move(50, 200)
        self.tv_data.clicked.connect(self.open_tv_data)

        self.movie_data.setText('Movie Data')
        self.movie_data.resize(150, 50)
        self.movie_data.move(50, 250)
        # self.movie_data.clicked.connect(self.open_movie_data)

        self.tv_table_window = 0
        self.movie_table_window = 0

    def open_tv_data(self):
        test_dict = {1: {'rank': '2', 'rankChange': '+3', 'title': 'Test Show'}, 2: {'rank': '1', 'rankChange': '-6',
                                                                                     'title': 'Test Show2'}}
        tv_table = TvTable(test_dict)
        self.tv_table_window = TableWindow(tv_table)
        self.tv_table_window.show()


class TableWindow(QMainWindow):
    def __init__(self, table: QTableWidget):
        super().__init__()
        self.table = table
        self.setWindowTitle(self.table.title)
        self.setGeometry(500, 500, 400, 600)
        self.setFixedSize(400, 600)
        self.setCentralWidget(self.table)


class TvTable(QTableWidget):
    def __init__(self, tv_data: dict):
        super().__init__()
        self.tv_data = tv_data
        self.title = 'Most Popular Tv Table'
        self.width = 400
        self.height = 600
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)

        self.create_tv_table()

    def create_tv_table(self):
        self.setRowCount(len(self.tv_data))
        self.setColumnCount(3)

        for i in self.tv_data:
            self.setItem(i-1, 0, QTableWidgetItem(self.tv_data[i]['rank']))
            self.setItem(i-1, 1, QTableWidgetItem(self.tv_data[i]['rankChange']))
            self.setItem(i-1, 2, QTableWidgetItem(self.tv_data[i]['title']))
        self.move(0, 0)
