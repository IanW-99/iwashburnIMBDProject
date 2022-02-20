import sys
import secrets
import requests
import sqlite3


def main():
    top250TvData = get_top_250_tv()
    showIDs = get_show_ID(top250TvData)
    ratingTvData = get_ratings(showIDs)
    mostPopularTvData = get_most_popular_tv()
    top250MoviesData = get_top_250_movies()
    mostPopularMoviesData = get_most_popular_movies()
    mostChangedMovies = get_movie_IDs(mostPopularMoviesData)
    ratingMoviesData = get_ratings(mostChangedMovies)
    conn, curs = db_connect('imDataBase.db')
    create_dataBase_tables(curs)
    fill_top_250_tv_table(conn, curs, top250TvData)
    fill_rating_tv_table(conn, curs, ratingTvData)
    fill_most_popular_tv_table(conn, curs, mostPopularTvData)
    fill_top_250_movie_table(conn, curs, top250MoviesData)
    fill_most_popular_movies_table(conn, curs, mostPopularMoviesData)
    fill_rating_movies_table(conn, curs, ratingMoviesData)


def get_top_250_tv():
    response = requests.get(f"https://imdb-api.com/en/API/Top250TVs/{secrets.imdbKey}")
    try:
        json_data = response.json()
        return json_data
    except ValueError:
        print('No Response from API')


def get_show_ID(top250Data):
    showIDs = []
    for i in top250Data["items"]:
        if int(i["rank"]) == 1 or int(i["rank"]) == 50 or int(i["rank"]) == 100 or int(i["rank"]) == 200:
            showID = i["id"]
            showIDs.append(showID)
    return showIDs


def get_ratings(showIDs):
    user_ratings = []
    for showID in showIDs:
        response = requests.get(f"https://imdb-api.com/en/API/UserRatings/{secrets.imdbKey}/{showID}")
        json_data = response.json()
        user_ratings.append(json_data)
    return user_ratings


def get_most_popular_tv():
    response = requests.get(f"https://imdb-api.com/en/API/MostPopularTVs/{secrets.imdbKey}")
    try:
        json_data = response.json()
        return json_data
    except ValueError:
        print('No Response from API')


def get_top_250_movies():
    response = requests.get(f"https://imdb-api.com/en/API/Top250Movies/{secrets.imdbKey}")
    try:
        json_data = response.json()
        return json_data
    except ValueError:
        print('No Response from API')


def get_most_popular_movies():
    response = requests.get(f"https://imdb-api.com/en/API/MostPopularMovies/{secrets.imdbKey}")
    try:
        json_data = response.json()
        return json_data
    except ValueError:
        print('No Response from API')


def get_movie_IDs(mostPopularMovies):
    rank1 = ('randomId', -sys.maxsize - 1)
    rank2 = ('randomId2', -sys.maxsize - 1)
    rank3 = ('randomId3', -sys.maxsize - 1)
    lowestRank = ('randomId4', sys.maxsize)

    for key in mostPopularMovies["items"]:
        try:
            rankChange = int(key["rankUpDown"].replace(',', ''))
            if rankChange > rank3[1]:
                if rankChange > rank2[1]:
                    if rankChange > rank1[1]:
                        rank3 = rank2
                        rank2 = rank1
                        rank1 = (key["id"], rankChange)
                    else:
                        rank3 = rank2
                        rank2 = (key["id"], rankChange)
                else:
                    rank3 = (key["id"], rankChange)
            elif rankChange < lowestRank[1]:
                lowestRank = (key["id"], rankChange)
        except ValueError:
            pass
    movieIds = [rank1[0], rank2[0], rank3[0], lowestRank[0]]
    return movieIds


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


def fill_top_250_tv_table(conn: sqlite3.Connection, curs: sqlite3.Cursor, top250Tv):
    for item in top250Tv["items"]:
        insert_statement = '''INSERT OR IGNORE INTO top250TvData (id, rank, title, fullTitle, year, crew, imdbRating,
                            imdbRatingCount) VALUES (?,?,?,?,?,?,?,?)'''

        data = item["id"], item["rank"], item["title"], item["fullTitle"], item["year"], item["crew"],\
            item["imDbRating"], item["imDbRatingCount"]
        curs.execute(insert_statement, data)
        conn.commit()


def fill_rating_tv_table(conn: sqlite3.Connection, curs: sqlite3.Cursor, ratingData):
    for item in ratingData:
        ratings = item["ratings"]
        if ratings is not None and len(ratings) == 10:
            insert_statement = '''INSERT OR IGNORE INTO ratingTvData (id, totalRating, totalRatingVotes, \
            tenRatingPercent, tenRatingVotes, nineRatingPercent, nineRatingVotes, \
            eightRatingPercent, eightRatingVotes, sevenRatingPercent, sevenRatingVotes, \
            sixRatingPercent, sixRatingVotes, fiveRatingPercent, fiveRatingVotes, \
            fourRatingPercent, fourRatingVotes, threeRatingPercent, threeRatingVotes, \
            twoRatingPercent, twoRatingVotes, oneRatingPercent, oneRatingVotes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?)'''

            data = item["imDbId"], item["totalRating"], item["totalRatingVotes"], ratings[0]["percent"], \
                ratings[0]["votes"], ratings[1]["percent"], ratings[1]["votes"], ratings[2]["percent"], \
                ratings[2]["votes"], ratings[3]["percent"], ratings[3]["votes"], ratings[4]["percent"],\
                ratings[4]["votes"], ratings[5]["percent"], ratings[5]["votes"], ratings[6]["percent"],\
                ratings[6]["votes"], ratings[7]["percent"], ratings[7]["votes"], ratings[8]["percent"],\
                ratings[8]["votes"], ratings[9]["percent"], ratings[9]["votes"]
            curs.execute(insert_statement, data)
            conn.commit()


def fill_most_popular_tv_table(conn: sqlite3.Connection, curs: sqlite3.Cursor, most_popular_tv_data):
    for item in most_popular_tv_data["items"]:
        insert_statement = '''INSERT OR IGNORE INTO topTvData(id, rank, rankUpDown, title, fullTitle, year, crew,
         imdbRating, imdbRatingCount) VALUES (?,?,?,?,?,?,?,?,?)'''

        data = item["id"], item["rank"], item["rankUpDown"], item["title"], item["fullTitle"], \
            item["year"], item["crew"], item["imDbRating"], item["imDbRatingCount"]
        curs.execute(insert_statement, data)
        conn.commit()


def fill_top_250_movie_table(conn: sqlite3.Connection, curs: sqlite3.Cursor, top250Movies):
    for item in top250Movies["items"]:
        insert_statement = '''INSERT OR IGNORE INTO top250MoviesData (id, rank, title, fullTitle, year, crew,
            imdbRating,imdbRatingCount) VALUES (?,?,?,?,?,?,?,?)'''

        data = item["id"], item["rank"], item["title"], item["fullTitle"], \
            item["year"], item["crew"], item["imDbRating"], item["imDbRatingCount"]
        curs.execute(insert_statement, data)
        conn.commit()


def fill_most_popular_movies_table(conn: sqlite3.Connection, curs: sqlite3.Cursor, mostPopularMovies):
    for item in mostPopularMovies["items"]:
        insert_statement = '''INSERT OR IGNORE INTO topMoviesData(id, rank, rankUpDown, title, fullTitle, year, crew,
         imdbRating, imdbRatingCount) VALUES (?,?,?,?,?,?,?,?,?)'''

        data = item["id"], item["rank"], item["rankUpDown"], item["title"], item["fullTitle"], \
            item["year"], item["crew"], item["imDbRating"], item["imDbRatingCount"]
        curs.execute(insert_statement, data)
        conn.commit()


def fill_rating_movies_table(conn: sqlite3.Connection, curs: sqlite3.Cursor, ratingData):
    for item in ratingData:
        ratings = item["ratings"]
        if ratings is not None and len(ratings) == 10:
            insert_statement = '''INSERT OR IGNORE INTO ratingMoviesData (id, totalRating, totalRatingVotes, \
            tenRatingPercent, tenRatingVotes, nineRatingPercent, nineRatingVotes, \
            eightRatingPercent, eightRatingVotes, sevenRatingPercent, sevenRatingVotes, \
            sixRatingPercent, sixRatingVotes, fiveRatingPercent, fiveRatingVotes, \
            fourRatingPercent, fourRatingVotes, threeRatingPercent, threeRatingVotes, \
            twoRatingPercent, twoRatingVotes, oneRatingPercent, oneRatingVotes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?)'''

            data = item["imDbId"], item["totalRating"], item["totalRatingVotes"], ratings[0]["percent"], \
                ratings[0]["votes"], ratings[1]["percent"], ratings[1]["votes"], ratings[2]["percent"], \
                ratings[2]["votes"], ratings[3]["percent"], ratings[3]["votes"], ratings[4]["percent"], \
                ratings[4]["votes"], ratings[5]["percent"], ratings[5]["votes"], ratings[6]["percent"], \
                ratings[6]["votes"], ratings[7]["percent"], ratings[7]["votes"], ratings[8]["percent"], \
                ratings[8]["votes"], ratings[9]["percent"], ratings[9]["votes"]
            curs.execute(insert_statement, data)
            conn.commit()


main()
