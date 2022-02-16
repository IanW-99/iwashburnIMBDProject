import secrets
import requests
import sqlite3

#comment to fail build


def main():
    #top250TvData = getTop250Tv()
    #showIDs = getShowID(top250TvData)
    #ratingData = getRatings(showIDs)
    #mostPopularTvData = getMostPopularTv()
    #top250MoviesData = getTop250Movies()
    #writeToOutput(ratingData, top250TvData, mostPopularTvData, top250MoviesData)
    top250TvDict, ratingDict, mostPopularTvDict, top250MoviesDict = createDictionaries()
    conn, curs = dbConnect('imDataBase.db')
    createDataBase(curs)
    fillTop250TvData(conn, curs, top250TvDict)
    fillRatingData(conn, curs, ratingDict)
    fillMostPopularTvData(conn, curs, mostPopularTvDict)
    fillTop250MovieData(conn, curs, top250MoviesDict)


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
    wotRatings = requests.get(f"https://imdb-api.com/en/API/UserRatings/{secrets.imdbKey}/tt0331080")
    wot_data = wotRatings.json()
    user_ratings.append(wot_data)

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


def writeToOutput(ratingData, top250TvData, mostPopularTvData, top250MoviesData):
    with open('ratingData.txt', 'w') as f:
        for i in ratingData:
            output_data = f'{i["imDbId"]} | {i["totalRating"]} | {i["totalRatingVotes"]}'
            if i["ratings"] is not None:
                for j in i["ratings"]:
                    output_data += f' | {j["percent"]} | {j["votes"]}'
                output_data += '\n'
                f.write(output_data)

    with open('top250Tv.txt', 'w') as f:
        for i in top250TvData['items']:
            output_data = f'{i["id"]} | {i["rank"]} | {i["title"]} | {i["fullTitle"]} | {i["year"]} | {i["crew"]} |  ' \
                          f'{i["imDbRating"]} | {i["imDbRatingCount"]} \n'
            f.write(output_data)

    with open('mostPopularTv.txt', 'w') as f:
        for i in mostPopularTvData['items']:
            output_data = f'{i["id"]} | {i["rank"]} | {i["rankUpDown"]} | {i["title"]} | {i["fullTitle"]} | ' \
                          f'{i["year"]} | {i["crew"]} | {i["imDbRating"]} | {i["imDbRatingCount"]} \n'
            f.write(output_data)

    with open('top250Movies.txt', 'w') as f:
        for i in top250MoviesData['items']:
            output_data = f'{i["id"]} | {i["rank"]} | {i["title"]} | {i["fullTitle"]} | {i["year"]} | {i["crew"]} |  ' \
                          f'{i["imDbRating"]} | {i["imDbRatingCount"]} \n'
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
    curs.execute('''CREATE TABLE IF NOT EXISTS "ratingData" (
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


def createDictionaries():
    top250TvDict = {}
    ratingDict = {}
    mostPopularTvDict = {}
    top250MoviesDict = {}

    with open("top250Tv.txt", 'r') as dataFile:
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

    with open("ratingData.txt", 'r') as dataFile:
        for line in dataFile:
            parsedLine = line.strip().split(" | ")
            if len(parsedLine) == 23:
                ratingDict[parsedLine[0]] = {}
                ratingDict[parsedLine[0]]["totalRating"] = parsedLine[1]
                ratingDict[parsedLine[0]]["totalRatingVotes"] = parsedLine[2]
                ratingDict[parsedLine[0]]["tenRatingPercent"] = parsedLine[3]
                ratingDict[parsedLine[0]]["tenRatingVotes"] = parsedLine[4]
                ratingDict[parsedLine[0]]["nineRatingPercent"] = parsedLine[5]
                ratingDict[parsedLine[0]]["nineRatingVotes"] = parsedLine[6]
                ratingDict[parsedLine[0]]["eightRatingPercent"] = parsedLine[7]
                ratingDict[parsedLine[0]]["eightRatingVotes"] = parsedLine[8]
                ratingDict[parsedLine[0]]["sevenRatingPercent"] = parsedLine[9]
                ratingDict[parsedLine[0]]["sevenRatingVotes"] = parsedLine[10]
                ratingDict[parsedLine[0]]["sixRatingPercent"] = parsedLine[11]
                ratingDict[parsedLine[0]]["sixRatingVotes"] = parsedLine[12]
                ratingDict[parsedLine[0]]["fiveRatingPercent"] = parsedLine[13]
                ratingDict[parsedLine[0]]["fiveRatingVotes"] = parsedLine[14]
                ratingDict[parsedLine[0]]["fourRatingPercent"] = parsedLine[15]
                ratingDict[parsedLine[0]]["fourRatingVotes"] = parsedLine[16]
                ratingDict[parsedLine[0]]["threeRatingPercent"] = parsedLine[17]
                ratingDict[parsedLine[0]]["threeRatingVotes"] = parsedLine[18]
                ratingDict[parsedLine[0]]["twoRatingPercent"] = parsedLine[19]
                ratingDict[parsedLine[0]]["twoRatingVotes"] = parsedLine[20]
                ratingDict[parsedLine[0]]["oneRatingPercent"] = parsedLine[21]
                ratingDict[parsedLine[0]]["oneRatingVotes"] = parsedLine[22]

    with open('mostPopularTv.txt', 'r') as dataFile:
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

    with open("top250Movies.txt", 'r') as dataFile:
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

    return top250TvDict, ratingDict, mostPopularTvDict, top250MoviesDict


def fillTop250TvData(conn: sqlite3.Connection, curs: sqlite3.Cursor, top250Dict):
    for key in top250Dict:
        insert_statement = '''INSERT OR IGNORE INTO top250TvData (id, rank, title, fullTitle, year, crew, imdbRating,
                            imdbRatingCount) VALUES (?,?,?,?,?,?,?,?)'''

        data = key, top250Dict[key]["rank"], top250Dict[key]["title"], top250Dict[key]["fullTitle"], \
            top250Dict[key]["year"], top250Dict[key]["crew"], \
            top250Dict[key]["imdbRating"], top250Dict[key]["imdbRatingCount"]
        curs.execute(insert_statement, data)
        conn.commit()


def fillRatingData(conn: sqlite3.Connection, curs: sqlite3.Cursor, ratingDict):
    for key in ratingDict:
        insert_statement = '''INSERT OR IGNORE INTO ratingData (id, totalRating, totalRatingVotes, \
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
        insert_statement = '''INSERT OR IGNORE INTO top250MoviesData (id, rank, title, fullTitle, year, crew, imdbRating,
                            imdbRatingCount) VALUES (?,?,?,?,?,?,?,?)'''

        data = key, top250MoviesDict[key]["rank"], top250MoviesDict[key]["title"], top250MoviesDict[key]["fullTitle"], \
            top250MoviesDict[key]["year"], top250MoviesDict[key]["crew"], \
            top250MoviesDict[key]["imdbRating"], top250MoviesDict[key]["imdbRatingCount"]
        curs.execute(insert_statement, data)
        conn.commit()


main()
