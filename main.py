import secrets
import requests


def main():
    top250Data = getTop250Tv()
    showIDs = getShowID(top250Data)
    ratingData = getRatings(showIDs)
    writeToOutput(ratingData, top250Data)


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
    with open('top250.txt', 'w') as f:
        for i in ratingData:
            output_data = f'{i} \n'
            f.write(output_data)

        for i in top250Data['items']:
            output_data = f'{i["rank"]}) {i["fullTitle"]} \n \t id: {i["id"]} \n'
            f.write(output_data)


main()
