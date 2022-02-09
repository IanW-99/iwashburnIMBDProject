import secrets
import requests
import sqlite3


def main():
    # top250Data = getTop250Tv()
    # showIDs = getShowID(top250Data)
    # ratingData = getRatings(showIDs)
    # writeToOutput(ratingData, top250Data)
    conn, curs = dbConnect()
    createDataBase(curs)
    fillHeadlineData(curs)


def getTop250Tv():
    response = requests.get(f"https://imdb-api.com/en/API/Top250TVs/{secrets.imbdKey}")
    json_data = response.json()
    return json_data


def getShowID(top250Data):
    showIDs = []
    for i in top250Data["items"]:
        if int(i["rank"]) == 1 or int(i["rank"]) == 50 or int(i["rank"]) == 100 or int(i["rank"]) == 200:
            showID = i["id"]
            showIDs.append(showID)
    return showIDs


def getRatings(showIDs):
    user_rankings = []
    for showID in showIDs:
        response = requests.get(f"https://imdb-api.com/en/API/UserRatings/{secrets.imbdKey}/{showID}")
        json_data = response.json()
        user_rankings.append(json_data)
    wotRatings = requests.get(f"https://imdb-api.com/en/API/UserRatings/{secrets.imbdKey}/tt0331080")
    wot_data = wotRatings.json()
    user_rankings.append(wot_data)

    return user_rankings


def writeToOutput(ratingData, top250Data):
    with open('ratingData.txt', 'w') as f:
        for i in ratingData:
            output_data = f'{i} \n'
            f.write(output_data)

    with open('top250.txt', 'w') as f:
        for i in top250Data['items']:
            output_data = f'{i["id"]} | {i["title"]} | {i["fullTitle"]} | {i["year"]}, | {i["crew"]} |  ' \
                          f'{i["imDbRating"]} | {i["imDbRatingCount"]}\n'
            f.write(output_data)


def dbConnect():
    conn = sqlite3.connect('imDataBase.db')
    curs = conn.cursor()
    return conn, curs


def createDataBase(curs: sqlite3.Cursor):
    curs.execute('''CREATE TABLE IF NOT EXISTS "headlineData" (
                        "id"	INTEGER,
                        "title"	TEXT,
                        "fullTitle"	TEXT,
                        "year"	INTEGER,
                        "crew"	BLOB,
                        "imdbRating"	NUMERIC,
                        "imdbRatingCount"	NUMERIC,
                        PRIMARY KEY("id"));''')
    curs.execute('''CREATE TABLE IF NOT EXISTS "ratingData" (
                        "id"	INTEGER,
                        "totalRating"	NUMERIC,
                        "totalRatingVotes"	INTEGER,
                        "tenRatingPercent"	NUMERIC,
                        "tenRatingVotes"	INTEGER,
                        "nineRatingPercent"	REAL,
                        "nineRatingVotes"	INTEGER,
                        "eightRatingPercent"	NUMERIC,
                        "eightRatingVotes"	INTEGER,
                        "sevenRatingPercent"	NUMERIC,
                        "sevenRatingVotes"	INTEGER,
                        "sixRatingPercent"	NUMERIC,
                        "sixRatingVotes"	INTEGER,
                        "fiveRatingPercent"	NUMERIC,
                        "fiveRatingVotes"	INTEGER,
                        "fourRatingPercent"	NUMERIC,
                        "fourRatingVotes"	INTEGER,
                        "threeRatingPercent"	NUMERIC,
                        "threeRatingVotes"	INTEGER,
                        "twoRatingPercent"	NUMERIC,
                        "twoRatingVotes"	INTEGER,
                        "oneRatingPercent"	NUMERIC,
                        "oneRatingVotes"	INTEGER,
                        PRIMARY KEY("id"));''')


def fillHeadlineData(curs: sqlite3.Cursor):
    dataDict = {}

    dataFile = open("top250.txt", 'r')
    for line in dataFile:
        key, title, fullTitle, year, crew, imdbRating, imdbRatingCount = line.split(" | ")
        dataDict[key] = {"title": {title.strip()}, "fullTitle": {fullTitle.strip()}, "year": {year.strip()},
                         "crew": {crew.strip()}, "imdbRating": {imdbRating.strip()},
                         "imdbRatingCount": {imdbRatingCount.strip()}}
    print(dataDict)


main()
