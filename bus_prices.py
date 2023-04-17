import requests
import json
import sqlite3

conn = sqlite3.connect("c:/Programing/Python/Start_Python/flixbus/uuids.db")

cursor = conn.cursor()

with open("c:/Programing/Python/Start_Python/flixbus/request.json", "r") as f:
    request = json.load(f)

flix_cities_request = requests.get(
    "https://global.api.flixbus.com/cms/cities", 
    params={"language": "en"}
    )
flix_cities =  flix_cities_request.json()["result"]

departure_cities_uuid = {}
for city in flix_cities:
    if city["slug"] in request["departure_cities"]:
        departure_cities_uuid[city["slug"]] = city["uuid"]
        cursor.execute(f'''INSERT INTO UUIDS VALUES ('{city["uuid"]}', '{city["slug"]}')''')

print(departure_cities_uuid)

with open(
    "c:/Programing/Python/Start_Python/flixbus/cities_uuids.json", 
    "a") as f:
    f.write(json.dumps(departure_cities_uuid))

conn.commit()
conn.close()

