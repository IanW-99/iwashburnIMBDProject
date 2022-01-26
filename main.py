import json
import secrets
import requests


def main():
    getTop250Tv()


def getTop250Tv():
    response = requests.get(f"https://imdb-api.com/en/API/Top250TVs/{secrets.imbdKey}")
    text = json.dumps(response.json(), sort_keys=True, indent=2)
    with open('top250.txt', 'w') as t:
        t.write(text)


main()
