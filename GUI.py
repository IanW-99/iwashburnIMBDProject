import sqlite3
from PyQt5.QtWidgets import QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout
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
        self.setGeometry(400, 400, 400, 300)
        self.setFixedSize(400, 150)

        self.update_data_button.setText("Update Data")
        self.update_data_button.resize(150, 50)
        self.update_data_button.move(50, 50)
        self.update_data_button.clicked.connect(self.update_data)

        self.data_visualization_menu_button.setText("Data Visualization")
        self.data_visualization_menu_button.resize(150, 50)
        self.data_visualization_menu_button.move(200, 50)
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
        self.setGeometry(400, 400, 400, 150)
        self.setFixedSize(400, 150)

        self.tv_data_open = False
        self.tv_data = QPushButton(self)
        self.movie_data_open = False
        self.movie_data = QPushButton(self)

        self.tv_data.setText('Tv Data')
        self.tv_data.resize(150, 50)
        self.tv_data.move(50, 50)
        self.tv_data.clicked.connect(self.open_tv_data)

        self.movie_data.setText('Movie Data')
        self.movie_data.resize(150, 50)
        self.movie_data.move(200, 50)
        # self.movie_data.clicked.connect(self.open_movie_data)

        self.tv_table_window = 0
        self.movie_table_window = 0

    def open_tv_data(self):
        most_popular_tv_data = {}
        select_statement = """SELECT id, rank, rankUpDown, title FROM topTvData;"""
        self.curs.execute(select_statement)
        for row in self.curs:
            row_data = {row[0]: {'rank': row[1], 'rankUpDown': row[2], 'title': row[3]}}
            most_popular_tv_data.update(row_data)

        tv_table = TvTable(most_popular_tv_data)
        self.tv_table_window = TableWindow(tv_table)
        self.tv_table_window.show()


class TableWindow(QMainWindow):
    def __init__(self, table: QTableWidget):
        super().__init__()
        self.table = table
        self.setWindowTitle(self.table.title)
        self.setGeometry(400, 400, 500, 600)
        self.setFixedSize(500, 600)

        self.sort_by_rank = QPushButton('Sort by Rank')
        self.sort_by_rank.clicked.connect(table.sort_by_rank)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.sort_by_rank)
        self.layout.addWidget(self.table)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)


class TvTable(QTableWidget):
    def __init__(self, tv_data: dict):
        super().__init__()
        self.tv_data = tv_data
        self.title = 'Most Popular Tv Table'
        self.column_labels = ['Rank', 'Rank Change', 'Show Title', 'Show ID']

        self.width = 500
        self.height = 600
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)

        self.create_tv_table()

    def create_tv_table(self):
        self.setRowCount(len(self.tv_data))
        self.setColumnCount(4)
        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 250)
        self.setColumnWidth(3, 100)
        self.setHorizontalHeaderLabels(self.column_labels)
        self.verticalHeader().setVisible(False)
        self.setSortingEnabled(False)
        self.fill_table(self.tv_data.keys())
        self.move(0, 0)

    def fill_table(self, keys):
        i = 0
        for key in keys:
            self.setItem(i, 0, QTableWidgetItem(self.tv_data[key]['rank']))
            print('got here')
            self.setItem(i, 1, QTableWidgetItem(self.tv_data[key]['rankUpDown']))
            self.setItem(i, 2, QTableWidgetItem(self.tv_data[key]['title']))
            self.setItem(i, 3, QTableWidgetItem(key))
            i += 1

    def sort_by_rank(self):
        sorted_keys = sorted(self.tv_data, key=lambda x: (self.tv_data[x]['rank']))
        self.fill_table(sorted_keys)
