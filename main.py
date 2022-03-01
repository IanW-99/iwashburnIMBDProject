import sys
import sqlite3
from PyQt5.QtWidgets import QApplication
import GUI


def main():
    conn, curs = db_connect('imDataBase.db')
    create_dataBase_tables(curs)

    app = QApplication(sys.argv)
    window = GUI.MainWindow(conn, curs)
    window.show()
    sys.exit(app.exec_())


def db_connect(filename):
    conn = sqlite3.connect(filename)
    curs = conn.cursor()
    return conn, curs


def create_dataBase_tables(curs: sqlite3.Cursor):
    curs.execute('''CREATE TABLE IF NOT EXISTS "top250TvData" (
                        "id"	    TEXT,
                        "rank"      TEXT,
                        "title"	    TEXT,
                        "fullTitle"	TEXT,
                        "year"	    TEXT,
                        "crew"	    TEXT,
                        "imdbRating"TEXT,
                        "imdbRatingCount"TEXT,
                        PRIMARY KEY("id"));''')
    curs.execute('''CREATE TABLE IF NOT EXISTS "ratingTvData" (
                        "id"    TEXT,
                        "totalRating"	    NUMERIC,
                        "totalRatingVotes"	INTEGER,
                        "tenRatingPercent"	NUMERIC,
                        "tenRatingVotes"	INTEGER,
                        "nineRatingPercent"	NUMERIC,
                        "nineRatingVotes"	INTEGER,
                        "eightRatingPercent"NUMERIC,
                        "eightRatingVotes"	INTEGER,
                        "sevenRatingPercent"NUMERIC,
                        "sevenRatingVotes"	INTEGER,
                        "sixRatingPercent"	NUMERIC,
                        "sixRatingVotes"	INTEGER,
                        "fiveRatingPercent"	NUMERIC,
                        "fiveRatingVotes"	INTEGER,
                        "fourRatingPercent"	NUMERIC,
                        "fourRatingVotes"	INTEGER,
                        "threeRatingPercent"NUMERIC,
                        "threeRatingVotes"	INTEGER,
                        "twoRatingPercent"	NUMERIC,
                        "twoRatingVotes"	INTEGER,
                        "oneRatingPercent"	NUMERIC,
                        "oneRatingVotes"	INTEGER,
                        PRIMARY KEY("id"));''')
    curs.execute('''CREATE TABLE IF NOT EXISTS "topTvData" (
                        "id"	        TEXT,
                        "rank"	        TEXT,
                        "rankUpDown"	TEXT,
                        "title"	        TEXT,
                        "fullTitle"	    TEXT,
                        "year"	        TEXT,
                        "crew"	        TEXT,
                        "imdbRating"	TEXT,
                        "imdbRatingCount"TEXT,
                        PRIMARY KEY("id"));''')
    curs.execute('''CREATE TABLE IF NOT EXISTS "top250MoviesData" (
                            "id"	    TEXT,
                            "rank"      TEXT,
                            "title"	    TEXT,
                            "fullTitle"	TEXT,
                            "year"	    TEXT,
                            "crew"	    TEXT,
                            "imdbRating"TEXT,
                            "imdbRatingCount"TEXT,
                            PRIMARY KEY("id"));''')
    curs.execute('''CREATE TABLE IF NOT EXISTS "topMoviesData" (
                            "id"	        TEXT,
                            "rank"	        TEXT,
                            "rankUpDown"	TEXT,
                            "title"	        TEXT,
                            "fullTitle"	    TEXT,
                            "year"	        TEXT,
                            "crew"	        TEXT,
                            "imdbRating"	TEXT,
                            "imdbRatingCount"TEXT,
                            PRIMARY KEY("id"));''')
    curs.execute('''CREATE TABLE IF NOT EXISTS "ratingMoviesData" (
                            "id"    TEXT,
                            "totalRating"	    NUMERIC,
                            "totalRatingVotes"	INTEGER,
                            "tenRatingPercent"	NUMERIC,
                            "tenRatingVotes"	INTEGER,
                            "nineRatingPercent"	NUMERIC,
                            "nineRatingVotes"	INTEGER,
                            "eightRatingPercent"NUMERIC,
                            "eightRatingVotes"	INTEGER,
                            "sevenRatingPercent"NUMERIC,
                            "sevenRatingVotes"	INTEGER,
                            "sixRatingPercent"	NUMERIC,
                            "sixRatingVotes"	INTEGER,
                            "fiveRatingPercent"	NUMERIC,
                            "fiveRatingVotes"	INTEGER,
                            "fourRatingPercent"	NUMERIC,
                            "fourRatingVotes"	INTEGER,
                            "threeRatingPercent"NUMERIC,
                            "threeRatingVotes"	INTEGER,
                            "twoRatingPercent"	NUMERIC,
                            "twoRatingVotes"	INTEGER,
                            "oneRatingPercent"	NUMERIC,
                            "oneRatingVotes"	INTEGER,
                            CONSTRAINT topMoviesData
                                FOREIGN KEY (id)
                                REFERENCES topMoviesData(id)
                            PRIMARY KEY("id"));''')


main()
