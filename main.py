import secrets
import requests
import sqlite3


# comment to test workflow

def main():
    # top250Data = getTop250Tv()
    # showIDs = getShowID(top250Data)
    # ratingData = getRatings(showIDs)
    # writeToOutput(ratingData, top250Data)
    top250Dict, ratingDict = createDictionaries()
    conn, curs = dbConnect('imDataBase.db')
    createDataBase(curs)
    fillHeadlineData(conn, curs, top250Dict)
    fillRatingData(conn, curs, ratingDict)


def getTop250Tv():
    response = requests.get(f"https://imdb-api.com/en/API/Top250TVs/{secrets.imbdKey}")
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
        response = requests.get(f"https://imdb-api.com/en/API/UserRatings/{secrets.imbdKey}/{showID}")
        json_data = response.json()
        user_ratings.append(json_data)
    wotRatings = requests.get(f"https://imdb-api.com/en/API/UserRatings/{secrets.imbdKey}/tt0331080")
    wot_data = wotRatings.json()
    user_ratings.append(wot_data)

    return user_ratings


def writeToOutput(ratingData, top250Data):
    with open('ratingData.txt', 'w') as f:
        for i in ratingData:
            output_data = f'{i["imDbId"]} | {i["totalRating"]} | {i["totalRatingVotes"]}'
            for j in i["ratings"]:
                output_data += f' | {j["percent"]} | {j["votes"]}'
            output_data += f'\n'
            f.write(output_data)

    with open('top250.txt', 'w') as f:
        for i in top250Data['items']:
            output_data = f'{i["id"]} | {i["title"]} | {i["fullTitle"]} | {i["year"]} | {i["crew"]} |  ' \
                          f'{i["imDbRating"]} | {i["imDbRatingCount"]} \n'
            f.write(output_data)


def dbConnect(filename):
    conn = sqlite3.connect(filename)
    curs = conn.cursor()
    return conn, curs


def createDataBase(curs: sqlite3.Cursor):
    curs.execute('''CREATE TABLE IF NOT EXISTS "headlineData" (
                        "id"	    TEXT,
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


def createDictionaries():
    top250Dict = {}
    ratingDict = {}

    with open("top250.txt", 'r') as dataFile:
        for line in dataFile:
            parsedLine = line.strip().split(" | ")
            top250Dict[parsedLine[0]] = {}
            top250Dict[parsedLine[0]]["title"] = parsedLine[1]
            top250Dict[parsedLine[0]]["fullTitle"] = parsedLine[2]
            top250Dict[parsedLine[0]]["year"] = parsedLine[3]
            top250Dict[parsedLine[0]]["crew"] = parsedLine[4]
            top250Dict[parsedLine[0]]["imdbRating"] = parsedLine[5]
            top250Dict[parsedLine[0]]["imdbRatingCount"] = parsedLine[6]

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
    return top250Dict, ratingDict


def fillHeadlineData(conn: sqlite3.Connection, curs: sqlite3.Cursor, top250Dict):
    for key in top250Dict:
        insert_statement = '''INSERT OR IGNORE INTO headlineData (id, title, fullTitle, year, crew, imdbRating,
                            imdbRatingCount) VALUES (?,?,?,?,?,?,?)'''

        data = key, top250Dict[key]["title"], top250Dict[key]["fullTitle"], top250Dict[key]["year"], top250Dict[key][
            "crew"], top250Dict[key]["imdbRating"], top250Dict[key]["imdbRatingCount"]
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


main()
