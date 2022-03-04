import sqlite3
from PyQt5.QtWidgets import QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, \
    QAbstractItemView, QMessageBox
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
        self.setGeometry(400, 400, 400, 400)
        self.setFixedSize(400, 400)

        self.tv_data_open = False
        self.tv_data = QPushButton(self)
        self.movie_data_open = False
        self.movie_data = QPushButton(self)

        self.tv_data.setText('Most Popular Tv Data')
        self.tv_data.resize(150, 50)
        self.tv_data.move(50, 50)
        self.tv_data.clicked.connect(self.open_tv_data)

        self.movie_data.setText('Most Popular Movie Data')
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

        tv_table = MostPopularTable(most_popular_tv_data, 0, self.conn, self.curs)
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

        movie_table = MostPopularTable(most_popular_movie_data, 1, self.conn, self.curs)
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

        self.get_selected_info = QPushButton('Get More Info on Selected Row')
        self.get_selected_info.clicked.connect(self.table.get_cell_info)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.sort_by_rank)
        self.layout.addWidget(self.sort_by_rank_change)
        self.layout.addWidget(self.get_selected_info)
        self.layout.addWidget(self.table)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)


class MostPopularTable(QTableWidget):
    def __init__(self, data: dict, table_type: int, conn: sqlite3.Connection, curs: sqlite3.Cursor):
        super().__init__()
        self.conn = conn
        self.curs = curs
        self.data = data
        self.table_type = table_type
        if self.table_type == 0:
            self.title = 'Most Popular Tv Table'
        else:
            self.title = ' Most Popular Movie Table'
        self.column_labels = ['Rank', 'Rank Change', 'Title', 'ID']

        self.width = 500
        self.height = 600

        self.select_msg = QMessageBox(self)
        self.select_msg.setWindowTitle('Selected Cell Info')
        self.select_msg.hide()

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

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
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
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

    def get_cell_info(self):
        if self.table_type == 0:
            self.make_popup_window('This only works for movies, sorry!', QMessageBox.Warning, (300, 300))
        else:
            if self.selectedItems():
                movie_id = self.selectedItems()[3].text()
                query = '''SELECT * FROM ratingMoviesData where id = ?'''
                data = movie_id,
                self.curs.execute(query, data)
                ratings = self.curs.fetchone()
                if ratings is not None:
                    msg = f"Total Rating: {ratings[1]}, Total Votes: {ratings[2]} \n" \
                          f"10 Rating Percent: {ratings[3]}, Votes: {ratings[4]} \n" \
                          f"9 Rating Percent: {ratings[5]}, Votes: {ratings[6]} \n" \
                          f"8 Rating Percent: {ratings[7]}, Votes: {ratings[8]} \n" \
                          f"7 Rating Percent: {ratings[9]}, Votes: {ratings[10]} \n" \
                          f"6 Rating Percent: {ratings[11]}, Votes: {ratings[12]} \n" \
                          f"5 Rating Percent: {ratings[13]}, Votes: {ratings[14]} \n" \
                          f"4 Rating Percent: {ratings[15]}, Votes: {ratings[16]} \n" \
                          f"3 Rating Percent: {ratings[17]}, Votes: {ratings[18]} \n" \
                          f"2 Rating Percent: {ratings[19]}, Votes: {ratings[20]} \n" \
                          f"1 Rating Percent: {ratings[21]}, Votes: {ratings[22]}"
                    self.make_popup_window(msg, QMessageBox.Information, (700, 300))
                else:
                    self.make_popup_window('No Rating Data Available', QMessageBox.Information, (300, 300))
            else:
                self.make_popup_window('You must select a row!', QMessageBox.Warning, (300, 300))

    def make_popup_window(self, msg, icon, size: tuple):
        self.select_msg.setText(msg)
        self.select_msg.setIcon(icon)
        self.select_msg.resize(size[0], size[1])
        self.select_msg.show()
