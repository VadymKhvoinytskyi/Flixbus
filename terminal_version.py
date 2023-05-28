import requests
import json


def get_trips(departure_names: list, arrival_names: list, dates: list,  dict_uuids: dict) -> list:
    result_trips = []
    i = 0
    n = len(departure_names) * len(arrival_names) * len(dates)

    for arrival_name in arrival_names:
        for departure_name in departure_names:

            arrival_uuid, departure_uuid = dict_uuids[arrival_name], dict_uuids[departure_name]
            for date in dates:
                url = f"https://global.api.flixbus.com/search/service/v4/search?from_city_id={departure_uuid}&to_city_id={arrival_uuid}&departure_date={date}&products=%7B%22adult%22%3A2%7D&currency=EUR&locale=en&search_by=cities&include_after_midnight_rides=1"
                response = requests.get(url)
                # print(response.status_code)
                print(f"{'#' * int(i // (n / 20))}")
                i += 1

                if response.status_code == 200:
                    response_json = response.json()["trips"][0]
                    results_json = response_json["results"]
                    
                    for key in results_json:
                        result_trips.append([
                            f"{departure_name} - {arrival_name}",
                            results_json[key]['price']['average'],
                            results_json[key]['departure']['date'],
                            results_json[key]['arrival']['date'],
                            f"https://shop.flixbus.ua/search?departureCity={departure_uuid}&arrivalCity={arrival_uuid}&rideDate={date}&adult=2&_locale=uk&features%5Bfeature.darken_page%5D=1&features%5Bfeature.enable_distribusion%5D=1&features%5Bfeature.train_cities_only%5D=0&features%5Bfeature.webc_search_persistent_explore_map%5D=0&atb_pdid=cc861ad2-ab97-43a7-971e-623e0c66e29f&_sp=1c858985-ce9b-4a8e-9e59-e4f41512f0b7&_spnuid=af71e384-6ff1-4a74-b031-8e7851f5e897"
                        ])
    return result_trips

if __name__ == "__main__":
    uuids = {
        "Duesseldorf": "40d911c7-8646-11e6-9066-549f350fcb0c",
        "Cologne": "40d91025-8646-11e6-9066-549f350fcb0c", 
        "Moenchengladbach": "40da838e-8646-11e6-9066-549f350fcb0c",
        "Paris": "40de8964-8646-11e6-9066-549f350fcb0c",
        "Amsterdam": "40dde3b8-8646-11e6-9066-549f350fcb0c",
        "Brussel": "40de6287-8646-11e6-9066-549f350fcb0c",
        "Barcelona": "40e086ed-8646-11e6-9066-549f350fcb0c",
        "Rotterdam": "40dee83e-8646-11e6-9066-549f350fcb0c",
        "Berlin": "40d8f682-8646-11e6-9066-549f350fcb0c",
        "Kyiv": "183cda51-3912-4707-95af-05238cd58ab8"
    }
    dates_departure = [f"{0 if i < 10 else ''}{i}.06.2023" for i in range(1, 10)]
    trips = get_trips(
        departure_names=["Duesseldorf", "Cologne", "Moenchengladbach"], 
        arrival_names=["Berlin"], 
        dates=dates_departure, 
        dict_uuids=uuids
        )
    trips = sorted(trips, key=lambda x: x[1], reverse=True)
    for trip in trips:
        print(trip, end='\n\n')
 