import sys
import secrets
import requests
import sqlite3


def main():
    top250TvData = getTop250Tv()
    showIDs = getShowID(top250TvData)
    ratingTvData = getRatings(showIDs)
    mostPopularTvData = getMostPopularTv()
    top250MoviesData = getTop250Movies()
    mostPopularMoviesData = getMostPopularMovies()
    mostChangedMovies = getMovieIDs(mostPopularMoviesData)
    ratingMoviesData = getRatings(mostChangedMovies)
    conn, curs = dbConnect('imDataBase.db')
    createDataBase(curs)
    fillTop250TvData(conn, curs, top250TvData)
    fillRatingTvData(conn, curs, ratingTvData)
    fillMostPopularTvData(conn, curs, mostPopularTvData)
    fillTop250MovieData(conn, curs, top250MoviesData)
    fillMostPopularMoviesData(conn, curs, mostPopularMoviesData)
    fillRatingMoviesData(conn, curs, ratingMoviesData)


def getTop250Tv():
    response = requests.get(f"https://imdb-api.com/en/API/Top250TVs/{secrets.imdbKey}")
    try:
        json_data = response.json()
        return json_data
    except ValueError:
        print('No Response from API')


def getShowID(top250Data):
    showIDs = []
    for i in top250Data["items"]:
        if int(i["rank"]) == 1 or int(i["rank"]) == 50 or int(i["rank"]) == 100 or int(i["rank"]) == 200:
            showID = i["id"]
            showIDs.append(showID)
    return showIDs


def getRatings(showIDs):
    user_ratings = []
    for showID in showIDs:
        response = requests.get(f"https://imdb-api.com/en/API/UserRatings/{secrets.imdbKey}/{showID}")
        json_data = response.json()
        user_ratings.append(json_data)
    return user_ratings


def getMostPopularTv():
    response = requests.get(f"https://imdb-api.com/en/API/MostPopularTVs/{secrets.imdbKey}")
    try:
        json_data = response.json()
        return json_data
    except ValueError:
        print('No Response from API')


def getTop250Movies():
    response = requests.get(f"https://imdb-api.com/en/API/Top250Movies/{secrets.imdbKey}")
    try:
        json_data = response.json()
        return json_data
    except ValueError:
        print('No Response from API')


def getMostPopularMovies():
    response = requests.get(f"https://imdb-api.com/en/API/MostPopularMovies/{secrets.imdbKey}")
    try:
        json_data = response.json()
        return json_data
    except ValueError:
        print('No Response from API')


def getMovieIDs(mostPopularMoviesDict):
    rank1 = ('randomId', -sys.maxsize-1)
    rank2 = ('randomId2', -sys.maxsize-1)
    rank3 = ('randomId3', -sys.maxsize-1)
    lowestRank = ('randomId4', sys.maxsize)

    for key in mostPopularMoviesDict["items"]:
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
    movieIds = [rank1[0], rank2[0], rank3[0], lowestRank[0]]
    return movieIds


def dbConnect(filename):
    conn = sqlite3.connect(filename)
    curs = conn.cursor()
    return conn, curs


def createDataBase(curs: sqlite3.Cursor):
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
                            PRIMARY KEY("id"));''')


def fillTop250TvData(conn: sqlite3.Connection, curs: sqlite3.Cursor, top250Dict):
    for key in top250Dict["items"]:
        insert_statement = '''INSERT OR IGNORE INTO top250TvData (id, rank, title, fullTitle, year, crew, imdbRating,
                            imdbRatingCount) VALUES (?,?,?,?,?,?,?,?)'''

        data = key, top250Dict[key]["rank"], top250Dict[key]["title"], top250Dict[key]["fullTitle"], \
            top250Dict[key]["year"], top250Dict[key]["crew"], \
            top250Dict[key]["imdbRating"], top250Dict[key]["imdbRatingCount"]
        curs.execute(insert_statement, data)
        conn.commit()


def fillRatingTvData(conn: sqlite3.Connection, curs: sqlite3.Cursor, ratingData):
    for key in ratingData:
        insert_statement = '''INSERT OR IGNORE INTO ratingTvData (id, totalRating, totalRatingVotes, \
        tenRatingPercent, tenRatingVotes, nineRatingPercent, nineRatingVotes, \
        eightRatingPercent, eightRatingVotes, sevenRatingPercent, sevenRatingVotes, \
        sixRatingPercent, sixRatingVotes, fiveRatingPercent, fiveRatingVotes, \
        fourRatingPercent, fourRatingVotes, threeRatingPercent, threeRatingVotes, \
        twoRatingPercent, twoRatingVotes, oneRatingPercent, oneRatingVotes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,
        ?,?,?,?,?,?,?,?,?)'''

        data = key, ratingData[key]["totalRating"], ratingData[key]["totalRatingVotes"], \
            ratingData[key]["tenRatingPercent"], ratingData[key]["tenRatingVotes"], \
            ratingData[key]["nineRatingPercent"], ratingData[key]["nineRatingVotes"], \
            ratingData[key]["eightRatingPercent"], ratingData[key]["eightRatingVotes"], \
            ratingData[key]["sevenRatingPercent"], ratingData[key]["sevenRatingVotes"], \
            ratingData[key]["sixRatingPercent"], ratingData[key]["sixRatingVotes"], \
            ratingData[key]["fiveRatingPercent"], ratingData[key]["fiveRatingVotes"], \
            ratingData[key]["fourRatingPercent"], ratingData[key]["fourRatingVotes"], \
            ratingData[key]["threeRatingPercent"], ratingData[key]["threeRatingVotes"], \
            ratingData[key]["twoRatingPercent"], ratingData[key]["twoRatingVotes"], \
            ratingData[key]["oneRatingPercent"], ratingData[key]["oneRatingVotes"]
        curs.execute(insert_statement, data)
        conn.commit()


def fillMostPopularTvData(conn: sqlite3.Connection, curs: sqlite3.Cursor, mostPopularTvDict):
    for key in mostPopularTvDict:
        insert_statement = '''INSERT OR IGNORE INTO topTvData(id, rank, rankUpDown, title, fullTitle, year, crew,
         imdbRating, imdbRatingCount) VALUES (?,?,?,?,?,?,?,?,?)'''

        data = key, mostPopularTvDict[key]["rank"], mostPopularTvDict[key]["rankUpDown"], \
            mostPopularTvDict[key]["title"], mostPopularTvDict[key]["fullTitle"], mostPopularTvDict[key]["year"], \
            mostPopularTvDict[key]["crew"], mostPopularTvDict[key]["imdbRating"], \
            mostPopularTvDict[key]["imdbRatingCount"]
        curs.execute(insert_statement, data)
        conn.commit()


def fillTop250MovieData(conn: sqlite3.Connection, curs: sqlite3.Cursor, top250MoviesDict):
    for key in top250MoviesDict:
        insert_statement = '''INSERT OR IGNORE INTO top250MoviesData (id, rank, title, fullTitle, year, crew,
                            imdbRating, imdbRatingCount) VALUES (?,?,?,?,?,?,?,?)'''

        data = key, top250MoviesDict[key]["rank"], top250MoviesDict[key]["title"], top250MoviesDict[key]["fullTitle"], \
            top250MoviesDict[key]["year"], top250MoviesDict[key]["crew"], \
            top250MoviesDict[key]["imdbRating"], top250MoviesDict[key]["imdbRatingCount"]
        curs.execute(insert_statement, data)
        conn.commit()


def fillMostPopularMoviesData(conn: sqlite3.Connection, curs: sqlite3.Cursor, mostPopularMoviesDict):
    for key in mostPopularMoviesDict:
        insert_statement = '''INSERT OR IGNORE INTO topMoviesData(id, rank, rankUpDown, title, fullTitle, year, crew,
         imdbRating, imdbRatingCount) VALUES (?,?,?,?,?,?,?,?,?)'''

        data = key, mostPopularMoviesDict[key]["rank"], mostPopularMoviesDict[key]["rankUpDown"], \
            mostPopularMoviesDict[key]["title"], mostPopularMoviesDict[key]["fullTitle"], \
            mostPopularMoviesDict[key]["year"], mostPopularMoviesDict[key]["crew"], \
            mostPopularMoviesDict[key]["imdbRating"], mostPopularMoviesDict[key]["imdbRatingCount"]
        curs.execute(insert_statement, data)
        conn.commit()


def fillRatingMoviesData(conn: sqlite3.Connection, curs: sqlite3.Cursor, ratingData):
    for key in ratingData:
        insert_statement = '''INSERT OR IGNORE INTO ratingMoviesData (id, totalRating, totalRatingVotes, \
        tenRatingPercent, tenRatingVotes, nineRatingPercent, nineRatingVotes, \
        eightRatingPercent, eightRatingVotes, sevenRatingPercent, sevenRatingVotes, \
        sixRatingPercent, sixRatingVotes, fiveRatingPercent, fiveRatingVotes, \
        fourRatingPercent, fourRatingVotes, threeRatingPercent, threeRatingVotes, \
        twoRatingPercent, twoRatingVotes, oneRatingPercent, oneRatingVotes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,
        ?,?,?,?,?,?,?,?,?)'''

        data = key, ratingData[key]["totalRating"], ratingData[key]["totalRatingVotes"], \
            ratingData[key]["tenRatingPercent"], ratingData[key]["tenRatingVotes"], \
            ratingData[key]["nineRatingPercent"], ratingData[key]["nineRatingVotes"], \
            ratingData[key]["eightRatingPercent"], ratingData[key]["eightRatingVotes"], \
            ratingData[key]["sevenRatingPercent"], ratingData[key]["sevenRatingVotes"], \
            ratingData[key]["sixRatingPercent"], ratingData[key]["sixRatingVotes"], \
            ratingData[key]["fiveRatingPercent"], ratingData[key]["fiveRatingVotes"], \
            ratingData[key]["fourRatingPercent"], ratingData[key]["fourRatingVotes"], \
            ratingData[key]["threeRatingPercent"], ratingData[key]["threeRatingVotes"], \
            ratingData[key]["twoRatingPercent"], ratingData[key]["twoRatingVotes"], \
            ratingData[key]["oneRatingPercent"], ratingData[key]["oneRatingVotes"]
        curs.execute(insert_statement, data)
        conn.commit()


main()
