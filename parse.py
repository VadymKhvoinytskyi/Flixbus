import requests
import json

'''TRIPS_ENDPOINT = "https://global.api.flixbus.com/search/service/v4/search"

paramateres = {"from_city_id": "40de8964-8646-11e6-9066-549f350fcb0c",
          "to_city_id": "40d911c7-8646-11e6-9066-549f350fcb0c",
          "departure_date": "23.04.2023",
          "products": r"%7B%22adult%22%3A2%7D",
          "currency": "EUR",
          "locale": "en",
          "search_by": "cities",
          "include_after_midnight_rides": 1}

response = requests.get(TRIPS_ENDPOINT, params=paramateres)'''

departure_uuids = ["40d91025-8646-11e6-9066-549f350fcb0c", "40d911c7-8646-11e6-9066-549f350fcb0c", "40da838e-8646-11e6-9066-549f350fcb0c"]

arrival_uuids = ["40e086ed-8646-11e6-9066-549f350fcb0c"]

dates = [f"{i}.05.2023" for i in range(10, 17)]



for arrival_uuid in arrival_uuids:

    with open(f"to_{arrival_uuid}.json", "a") as file:
        file.write('"result": [')

    for departure_uuid in departure_uuids:
        for date in dates:

            response = requests.get(f"https://global.api.flixbus.com/search/service/v4/search?from_city_id={departure_uuid}&to_city_id={arrival_uuid}&departure_date={date}&products=%7B%22adult%22%3A2%7D&currency=EUR&locale=en&search_by=cities&include_after_midnight_rides=1")

            print(response.status_code)
            print(response.text)

            with open(f"to_{arrival_uuid}.json", "a") as file:
                file.write(json.dumps(response.json()["trips"][0]["results"]))
                file.write(", ")

with open(f"to_{arrival_uuid}.json", "a") as file:
    file.write(']')


'''response = requests.get("https://global.api.flixbus.com/search/service/v4/search?from_city_id=40de8964-8646-11e6-9066-549f350fcb0c&to_city_id=40d911c7-8646-11e6-9066-549f350fcb0c&departure_date=23.04.2023&products=%7B%22adult%22%3A2%7D&currency=EUR&locale=en&search_by=cities&include_after_midnight_rides=1")

print(response.text)'''