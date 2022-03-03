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

    def update_data(self):  # need to drop all old data first
        self.curs.execute('''DELETE FROM ratingMoviesData;''')
        self.curs.execute('''DELETE FROM ratingTvData;''')
        self.curs.execute('''DELETE FROM top250MoviesData;''')
        self.curs.execute('''DELETE FROM top250TvData;''')
        self.curs.execute('''DELETE FROM topMoviesData;''')
        self.curs.execute('''DELETE FROM topTvData;''')
        self.conn.commit()
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
        self.movie_data.clicked.connect(self.open_movie_data)

        self.tv_table_window = 0
        self.movie_table_window = 0

    def open_tv_data(self):
        most_popular_tv_data = {}
        select_statement = """SELECT id, rank, rankUpDown, title FROM topTvData;"""
        self.curs.execute(select_statement)
        for row in self.curs:  # imdb api is trash and sends wrong rank change format sometimes
            clean_rankUpDown = row[2]
            if clean_rankUpDown[0].isdigit():
                clean_rankUpDown = "+" + clean_rankUpDown
            row_data = {row[0]: {'rank': row[1], 'rankUpDown': clean_rankUpDown, 'title': row[3]}}
            most_popular_tv_data.update(row_data)

        tv_table = Table(most_popular_tv_data, 0)
        self.tv_table_window = TableWindow(tv_table)
        self.tv_table_window.show()

    def open_movie_data(self):
        most_popular_movie_data = {}
        select_statement = """SELECT id, rank, rankUpDown, title FROM topMoviesData;"""
        self.curs.execute(select_statement)
        for row in self.curs:
            clean_rankUpDown = row[2]
            if clean_rankUpDown[0].isdigit():
                clean_rankUpDown = "+" + clean_rankUpDown
            row_data = {row[0]: {'rank': row[1], 'rankUpDown': clean_rankUpDown, 'title': row[3]}}
            most_popular_movie_data.update(row_data)

        movie_table = Table(most_popular_movie_data, 1)
        self.movie_table_window = TableWindow(movie_table)
        self.movie_table_window.show()


class TableWindow(QMainWindow):
    def __init__(self, table: QTableWidget):
        super().__init__()
        self.table = table
        self.setWindowTitle(self.table.title)
        self.setGeometry(400, 400, 500, 600)
        self.setFixedSize(500, 600)

        self.sort_by_rank = QPushButton('Sort by Rank')
        self.sort_by_rank.clicked.connect(self.table.sort_by_rank)

        self.sort_by_rank_change = QPushButton('Sort by Rank Change')
        self.sort_by_rank_change.clicked.connect(self.table.sort_by_rank_change)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.sort_by_rank)
        self.layout.addWidget(self.sort_by_rank_change)
        self.layout.addWidget(self.table)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)


class Table(QTableWidget):
    def __init__(self, data: dict, table_type: int):  # 0 = tv & 1 = movie
        super().__init__()
        self.data = data
        if table_type == 0:
            self.title = 'Most Popular Tv Table'
        else:
            self.title = ' Most Popular Movie Table'
        self.column_labels = ['Rank', 'Rank Change', 'Title', 'ID']

        self.width = 500
        self.height = 600
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)

        self.create_table()

    def create_table(self):
        self.setRowCount(len(self.data))
        self.setColumnCount(4)
        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 225)
        self.setColumnWidth(3, 75)
        self.setHorizontalHeaderLabels(self.column_labels)
        self.verticalHeader().setVisible(False)
        self.setSortingEnabled(False)
        self.fill_table(self.data.keys())

    def fill_table(self, keys):
        i = 0
        for key in keys:
            self.setItem(i, 0, QTableWidgetItem(self.data[key]['rank']))
            self.setItem(i, 1, QTableWidgetItem(self.data[key]['rankUpDown']))
            self.setItem(i, 2, QTableWidgetItem(self.data[key]['title']))
            self.setItem(i, 3, QTableWidgetItem(key))
            i += 1

    def sort_by_rank(self):
        sorted_keys = sorted(self.data, key=lambda x: (int(self.data[x]['rank'].replace(",", ""))))
        self.fill_table(sorted_keys)

    def sort_by_rank_change(self):
        sorted_keys = sorted(self.data, key=lambda x: (int(self.data[x]['rankUpDown'].replace(",", ""))), reverse=True)
        self.fill_table(sorted_keys)
