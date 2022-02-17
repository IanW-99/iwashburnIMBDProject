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
    writeToOutput(ratingTvData, top250TvData, mostPopularTvData, top250MoviesData, mostPopularMoviesData,
                  ratingMoviesData)
    top250TvDict, ratingTvDict, mostPopularTvDict, top250MoviesDict, mostPopularMoviesDict, ratingMoviesDict\
        = createDictionaries()
    conn, curs = dbConnect('imDataBase.db')
    createDataBase(curs)
    fillTop250TvData(conn, curs, top250TvDict)
    fillRatingTvData(conn, curs, ratingTvDict)
    fillMostPopularTvData(conn, curs, mostPopularTvDict)
    fillTop250MovieData(conn, curs, top250MoviesDict)
    fillMostPopularMoviesData(conn, curs, mostPopularMoviesDict)
    fillRatingMoviesData(conn, curs, ratingMoviesDict)


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


def writeToOutput(ratingTvData, top250TvData, mostPopularTvData, top250MoviesData, mostPopularMoviesData,
                  ratingMoviesData):
    with open('textFiles/ratingTvData.txt', 'w') as f:
        for i in ratingTvData:
            output_data = f'{i["imDbId"]} | {i["totalRating"]} | {i["totalRatingVotes"]}'
            if i["ratings"] is not None:
                for j in i["ratings"]:
                    output_data += f' | {j["percent"]} | {j["votes"]}'
                output_data += '\n'
                f.write(output_data)

    with open('textFiles/top250Tv.txt', 'w') as f:
        for i in top250TvData['items']:
            output_data = f'{i["id"]} | {i["rank"]} | {i["title"]} | {i["fullTitle"]} | {i["year"]} | {i["crew"]} |  ' \
                          f'{i["imDbRating"]} | {i["imDbRatingCount"]} \n'
            f.write(output_data)

    with open('textFiles/mostPopularTv.txt', 'w') as f:
        for i in mostPopularTvData['items']:
            output_data = f'{i["id"]} | {i["rank"]} | {i["rankUpDown"]} | {i["title"]} | {i["fullTitle"]} | ' \
                          f'{i["year"]} | {i["crew"]} | {i["imDbRating"]} | {i["imDbRatingCount"]} \n'
            f.write(output_data)

    with open('textFiles/top250Movies.txt', 'w') as f:
        for i in top250MoviesData['items']:
            output_data = f'{i["id"]} | {i["rank"]} | {i["title"]} | {i["fullTitle"]} | {i["year"]} | {i["crew"]} |  ' \
                          f'{i["imDbRating"]} | {i["imDbRatingCount"]} \n'
            f.write(output_data)

    with open('textFiles/mostPopularMovies.txt', 'w') as f:
        for i in mostPopularMoviesData['items']:
            output_data = f'{i["id"]} | {i["rank"]} | {i["rankUpDown"]} | {i["title"]} | {i["fullTitle"]} | ' \
                          f'{i["year"]} | {i["crew"]} | {i["imDbRating"]} | {i["imDbRatingCount"]} \n'
            f.write(output_data)

    with open('textFiles/ratingMoviesData.txt', 'w') as f:
        for i in ratingMoviesData:
            output_data = f'{i["imDbId"]} | {i["totalRating"]} | {i["totalRatingVotes"]}'
            if i["ratings"] is not None:
                for j in i["ratings"]:
                    output_data += f' | {j["percent"]} | {j["votes"]}'
                output_data += '\n'
                f.write(output_data)


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


def createDictionaries():
    top250TvDict = {}
    ratingTvDict = {}
    mostPopularTvDict = {}
    top250MoviesDict = {}
    mostPopularMoviesDict = {}
    ratingMoviesDict = {}

    with open("textFiles/top250Tv.txt", 'r') as dataFile:
        for line in dataFile:
            parsedLine = line.strip().split(" | ")
            top250TvDict[parsedLine[0]] = {}
            top250TvDict[parsedLine[0]]["rank"] = parsedLine[1]
            top250TvDict[parsedLine[0]]["title"] = parsedLine[2]
            top250TvDict[parsedLine[0]]["fullTitle"] = parsedLine[3]
            top250TvDict[parsedLine[0]]["year"] = parsedLine[4]
            top250TvDict[parsedLine[0]]["crew"] = parsedLine[5]
            top250TvDict[parsedLine[0]]["imdbRating"] = parsedLine[6]
            top250TvDict[parsedLine[0]]["imdbRatingCount"] = parsedLine[7]

    with open("textFiles/ratingTvData.txt", 'r') as dataFile:
        for line in dataFile:
            parsedLine = line.strip().split(" | ")
            if len(parsedLine) == 23:
                ratingTvDict[parsedLine[0]] = {}
                ratingTvDict[parsedLine[0]]["totalRating"] = parsedLine[1]
                ratingTvDict[parsedLine[0]]["totalRatingVotes"] = parsedLine[2]
                ratingTvDict[parsedLine[0]]["tenRatingPercent"] = parsedLine[3]
                ratingTvDict[parsedLine[0]]["tenRatingVotes"] = parsedLine[4]
                ratingTvDict[parsedLine[0]]["nineRatingPercent"] = parsedLine[5]
                ratingTvDict[parsedLine[0]]["nineRatingVotes"] = parsedLine[6]
                ratingTvDict[parsedLine[0]]["eightRatingPercent"] = parsedLine[7]
                ratingTvDict[parsedLine[0]]["eightRatingVotes"] = parsedLine[8]
                ratingTvDict[parsedLine[0]]["sevenRatingPercent"] = parsedLine[9]
                ratingTvDict[parsedLine[0]]["sevenRatingVotes"] = parsedLine[10]
                ratingTvDict[parsedLine[0]]["sixRatingPercent"] = parsedLine[11]
                ratingTvDict[parsedLine[0]]["sixRatingVotes"] = parsedLine[12]
                ratingTvDict[parsedLine[0]]["fiveRatingPercent"] = parsedLine[13]
                ratingTvDict[parsedLine[0]]["fiveRatingVotes"] = parsedLine[14]
                ratingTvDict[parsedLine[0]]["fourRatingPercent"] = parsedLine[15]
                ratingTvDict[parsedLine[0]]["fourRatingVotes"] = parsedLine[16]
                ratingTvDict[parsedLine[0]]["threeRatingPercent"] = parsedLine[17]
                ratingTvDict[parsedLine[0]]["threeRatingVotes"] = parsedLine[18]
                ratingTvDict[parsedLine[0]]["twoRatingPercent"] = parsedLine[19]
                ratingTvDict[parsedLine[0]]["twoRatingVotes"] = parsedLine[20]
                ratingTvDict[parsedLine[0]]["oneRatingPercent"] = parsedLine[21]
                ratingTvDict[parsedLine[0]]["oneRatingVotes"] = parsedLine[22]

    with open('textFiles/mostPopularTv.txt', 'r') as dataFile:
        for line in dataFile:
            parsedLine = line.strip().split(" | ")
            if len(parsedLine) == 9:
                mostPopularTvDict[parsedLine[0]] = {}
                mostPopularTvDict[parsedLine[0]]["rank"] = parsedLine[1]
                mostPopularTvDict[parsedLine[0]]["rankUpDown"] = parsedLine[2]
                mostPopularTvDict[parsedLine[0]]["title"] = parsedLine[3]
                mostPopularTvDict[parsedLine[0]]["fullTitle"] = parsedLine[4]
                mostPopularTvDict[parsedLine[0]]["year"] = parsedLine[5]
                mostPopularTvDict[parsedLine[0]]["crew"] = parsedLine[6]
                mostPopularTvDict[parsedLine[0]]["imdbRating"] = parsedLine[7]
                mostPopularTvDict[parsedLine[0]]["imdbRatingCount"] = parsedLine[8]

    with open("textFiles/top250Movies.txt", 'r') as dataFile:
        for line in dataFile:
            parsedLine = line.strip().split(" | ")
            top250MoviesDict[parsedLine[0]] = {}
            top250MoviesDict[parsedLine[0]]["rank"] = parsedLine[1]
            top250MoviesDict[parsedLine[0]]["title"] = parsedLine[2]
            top250MoviesDict[parsedLine[0]]["fullTitle"] = parsedLine[3]
            top250MoviesDict[parsedLine[0]]["year"] = parsedLine[4]
            top250MoviesDict[parsedLine[0]]["crew"] = parsedLine[5]
            top250MoviesDict[parsedLine[0]]["imdbRating"] = parsedLine[6]
            top250MoviesDict[parsedLine[0]]["imdbRatingCount"] = parsedLine[7]

    with open('textFiles/mostPopularMovies.txt', 'r') as dataFile:
        for line in dataFile:
            parsedLine = line.strip().split(" | ")
            if len(parsedLine) == 9:
                mostPopularMoviesDict[parsedLine[0]] = {}
                mostPopularMoviesDict[parsedLine[0]]["rank"] = parsedLine[1]
                mostPopularMoviesDict[parsedLine[0]]["rankUpDown"] = parsedLine[2]
                mostPopularMoviesDict[parsedLine[0]]["title"] = parsedLine[3]
                mostPopularMoviesDict[parsedLine[0]]["fullTitle"] = parsedLine[4]
                mostPopularMoviesDict[parsedLine[0]]["year"] = parsedLine[5]
                mostPopularMoviesDict[parsedLine[0]]["crew"] = parsedLine[6]
                mostPopularMoviesDict[parsedLine[0]]["imdbRating"] = parsedLine[7]
                mostPopularMoviesDict[parsedLine[0]]["imdbRatingCount"] = parsedLine[8]

    with open("textFiles/ratingMoviesData.txt", 'r') as dataFile:
        for line in dataFile:
            parsedLine = line.strip().split(" | ")
            if len(parsedLine) == 23:
                ratingMoviesDict[parsedLine[0]] = {}
                ratingMoviesDict[parsedLine[0]]["totalRating"] = parsedLine[1]
                ratingMoviesDict[parsedLine[0]]["totalRatingVotes"] = parsedLine[2]
                ratingMoviesDict[parsedLine[0]]["tenRatingPercent"] = parsedLine[3]
                ratingMoviesDict[parsedLine[0]]["tenRatingVotes"] = parsedLine[4]
                ratingMoviesDict[parsedLine[0]]["nineRatingPercent"] = parsedLine[5]
                ratingMoviesDict[parsedLine[0]]["nineRatingVotes"] = parsedLine[6]
                ratingMoviesDict[parsedLine[0]]["eightRatingPercent"] = parsedLine[7]
                ratingMoviesDict[parsedLine[0]]["eightRatingVotes"] = parsedLine[8]
                ratingMoviesDict[parsedLine[0]]["sevenRatingPercent"] = parsedLine[9]
                ratingMoviesDict[parsedLine[0]]["sevenRatingVotes"] = parsedLine[10]
                ratingMoviesDict[parsedLine[0]]["sixRatingPercent"] = parsedLine[11]
                ratingMoviesDict[parsedLine[0]]["sixRatingVotes"] = parsedLine[12]
                ratingMoviesDict[parsedLine[0]]["fiveRatingPercent"] = parsedLine[13]
                ratingMoviesDict[parsedLine[0]]["fiveRatingVotes"] = parsedLine[14]
                ratingMoviesDict[parsedLine[0]]["fourRatingPercent"] = parsedLine[15]
                ratingMoviesDict[parsedLine[0]]["fourRatingVotes"] = parsedLine[16]
                ratingMoviesDict[parsedLine[0]]["threeRatingPercent"] = parsedLine[17]
                ratingMoviesDict[parsedLine[0]]["threeRatingVotes"] = parsedLine[18]
                ratingMoviesDict[parsedLine[0]]["twoRatingPercent"] = parsedLine[19]
                ratingMoviesDict[parsedLine[0]]["twoRatingVotes"] = parsedLine[20]
                ratingMoviesDict[parsedLine[0]]["oneRatingPercent"] = parsedLine[21]
                ratingMoviesDict[parsedLine[0]]["oneRatingVotes"] = parsedLine[22]

    return top250TvDict, ratingTvDict, mostPopularTvDict, top250MoviesDict, mostPopularMoviesDict, ratingMoviesDict


def fillTop250TvData(conn: sqlite3.Connection, curs: sqlite3.Cursor, top250Dict):
    for key in top250Dict:
        insert_statement = '''INSERT OR IGNORE INTO top250TvData (id, rank, title, fullTitle, year, crew, imdbRating,
                            imdbRatingCount) VALUES (?,?,?,?,?,?,?,?)'''

        data = key, top250Dict[key]["rank"], top250Dict[key]["title"], top250Dict[key]["fullTitle"], \
            top250Dict[key]["year"], top250Dict[key]["crew"], \
            top250Dict[key]["imdbRating"], top250Dict[key]["imdbRatingCount"]
        curs.execute(insert_statement, data)
        conn.commit()


def fillRatingTvData(conn: sqlite3.Connection, curs: sqlite3.Cursor, ratingDict):
    for key in ratingDict:
        insert_statement = '''INSERT OR IGNORE INTO ratingTvData (id, totalRating, totalRatingVotes, \
        tenRatingPercent, tenRatingVotes, nineRatingPercent, nineRatingVotes, \
        eightRatingPercent, eightRatingVotes, sevenRatingPercent, sevenRatingVotes, \
        sixRatingPercent, sixRatingVotes, fiveRatingPercent, fiveRatingVotes, \
        fourRatingPercent, fourRatingVotes, threeRatingPercent, threeRatingVotes, \
        twoRatingPercent, twoRatingVotes, oneRatingPercent, oneRatingVotes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,
        ?,?,?,?,?,?,?,?,?)'''

        data = key, ratingDict[key]["totalRating"], ratingDict[key]["totalRatingVotes"], \
            ratingDict[key]["tenRatingPercent"], ratingDict[key]["tenRatingVotes"], \
            ratingDict[key]["nineRatingPercent"], ratingDict[key]["nineRatingVotes"], \
            ratingDict[key]["eightRatingPercent"], ratingDict[key]["eightRatingVotes"], \
            ratingDict[key]["sevenRatingPercent"], ratingDict[key]["sevenRatingVotes"], \
            ratingDict[key]["sixRatingPercent"], ratingDict[key]["sixRatingVotes"], \
            ratingDict[key]["fiveRatingPercent"], ratingDict[key]["fiveRatingVotes"], \
            ratingDict[key]["fourRatingPercent"], ratingDict[key]["fourRatingVotes"], \
            ratingDict[key]["threeRatingPercent"], ratingDict[key]["threeRatingVotes"], \
            ratingDict[key]["twoRatingPercent"], ratingDict[key]["twoRatingVotes"], \
            ratingDict[key]["oneRatingPercent"], ratingDict[key]["oneRatingVotes"]
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


def fillRatingMoviesData(conn: sqlite3.Connection, curs: sqlite3.Cursor, ratingDict):
    for key in ratingDict:
        insert_statement = '''INSERT OR IGNORE INTO ratingMoviesData (id, totalRating, totalRatingVotes, \
        tenRatingPercent, tenRatingVotes, nineRatingPercent, nineRatingVotes, \
        eightRatingPercent, eightRatingVotes, sevenRatingPercent, sevenRatingVotes, \
        sixRatingPercent, sixRatingVotes, fiveRatingPercent, fiveRatingVotes, \
        fourRatingPercent, fourRatingVotes, threeRatingPercent, threeRatingVotes, \
        twoRatingPercent, twoRatingVotes, oneRatingPercent, oneRatingVotes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,
        ?,?,?,?,?,?,?,?,?)'''

        data = key, ratingDict[key]["totalRating"], ratingDict[key]["totalRatingVotes"], \
            ratingDict[key]["tenRatingPercent"], ratingDict[key]["tenRatingVotes"], \
            ratingDict[key]["nineRatingPercent"], ratingDict[key]["nineRatingVotes"], \
            ratingDict[key]["eightRatingPercent"], ratingDict[key]["eightRatingVotes"], \
            ratingDict[key]["sevenRatingPercent"], ratingDict[key]["sevenRatingVotes"], \
            ratingDict[key]["sixRatingPercent"], ratingDict[key]["sixRatingVotes"], \
            ratingDict[key]["fiveRatingPercent"], ratingDict[key]["fiveRatingVotes"], \
            ratingDict[key]["fourRatingPercent"], ratingDict[key]["fourRatingVotes"], \
            ratingDict[key]["threeRatingPercent"], ratingDict[key]["threeRatingVotes"], \
            ratingDict[key]["twoRatingPercent"], ratingDict[key]["twoRatingVotes"], \
            ratingDict[key]["oneRatingPercent"], ratingDict[key]["oneRatingVotes"]
        curs.execute(insert_statement, data)
        conn.commit()


main()
