import json
import secrets
import requests


def main():
    getTop250Tv()


def getTop250Tv():
    response = requests.get(f"https://imdb-api.com/en/API/Top250TVs/{secrets.imbdKey}")
    json_data = response.json()

    with open('top250.txt', 'w') as f:
        for i in json_data['items']:
            output_data = f'{i["rank"]}) {i["fullTitle"]} \n \t id: {i["id"]} \n'
            f.write(output_data)


main()
