
import requests
from xml.etree import ElementTree
import time

# define the API URL and parameters
bggusername = "cteague3"
url = "https://www.boardgamegeek.com/xmlapi2/collection?username=" + bggusername+"&own=1&excludesubtype=boardgameexpansion&brief=0"

print(url)

# send the API request and parse the response
response = requests.get(url)
root = ElementTree.fromstring(response.content, parser=ElementTree.XMLParser())

# extract data from the response
games = []
for item in root.findall("item"):
    game_id = item.attrib["objectid"]
    game_url = "https://www.boardgamegeek.com/xmlapi2/thing?id="+game_id+"&stats=1"
    game_response = requests.get(game_url)
    #print(game_response)
    while game_response.status_code != 200: 
        #	print(game_response)
        time.sleep(3)
        game_response = requests.get(game_url)
    game_root = ElementTree.fromstring(game_response.content)
    #print(game_response)
    game = {}
    game["name"] = game_root.find("item/name").attrib["value"]
    game["id"] = game_id
    game["rating"] = game_root.find("item/statistics/ratings/average").attrib["value"]
    game["min_players"] = int(game_root.find("item/minplayers").attrib["value"])
    game["max_players"] = int(game_root.find("item/maxplayers").attrib["value"])
    if game["max_players"] >= 6:
         print(game["name"], game["id"],game["rating"],game["max_players"])
    games.append(game)

# print the list of games
print("Games ():")
for game in games:
    print(game["name"], game["id"],game["rating"])