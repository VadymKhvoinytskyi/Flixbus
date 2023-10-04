import requests
from pathlib import Path
import sqlite3
import pandas as pd
from datetime import datetime
from update_db import ask_add_data

def get_trips(departure_names: list[str], 
              arrival_names: list[str],  dict_uuids: dict[str: str], 
              dates: list[str]) -> list[list[str, str, float, str, str, str, str]]:
    
    result_trips = []
    i = 0
    n = len(departure_names) * len(arrival_names) * len(dates)

    for arrival_name in arrival_names:
        for departure_name in departure_names:
            arrival_uuid, departure_uuid = dict_uuids[arrival_name], dict_uuids[departure_name]
            for date in dates:
                url = f"https://global.api.flixbus.com/search/service/v4/search?from_city_id={departure_uuid}&to_city_id={arrival_uuid}&departure_date={date}&products=%7B%22adult%22%3A2%7D&currency=EUR&locale=en&search_by=cities&include_after_midnight_rides=1"
                response = requests.get(url)
                print(f"{'#' * int(i // (n / 20))}")
                i += 1

                if response.status_code == 200:
                    response_json = response.json()["trips"][0]
                    results_json = response_json["results"]
                    
                    for key in results_json:
                        result_trips.append([
                            departure_name,
                            arrival_name,
                            results_json[key]['price']['average'],
                            results_json[key]['departure']['date'],
                            results_json[key]['arrival']['date'],
                            results_json[key]['transfer_type_key'],
                            f"https://shop.flixbus.ua/search?departureCity={departure_uuid}&arrivalCity={arrival_uuid}&rideDate={date}&adult=2&_locale=uk&features%5Bfeature.darken_page%5D=1&features%5Bfeature.enable_distribusion%5D=1&features%5Bfeature.train_cities_only%5D=0&features%5Bfeature.webc_search_persistent_explore_map%5D=0&atb_pdid=cc861ad2-ab97-43a7-971e-623e0c66e29f&_sp=1c858985-ce9b-4a8e-9e59-e4f41512f0b7&_spnuid=af71e384-6ff1-4a74-b031-8e7851f5e897"
                        ])
    return result_trips


def get_uuids_from_db(departure_names: list[str], arrival_names: list[str], 
                      db = 'uuid_hash.db') -> dict[str: str]:
    cities = departure_names + arrival_names
    db_route = Path.cwd() / db
    con = sqlite3.connect(db_route)
    cur = con.cursor()
    res = cur.execute(f'SELECT * FROM UUIDS WHERE City in {tuple(cities)}')
    res = res.fetchall()
    con.commit()
    con.close()
    return dict(res)

def ask_cities(default = ["Duesseldorf", "Moenchengladbach", "Cologne", "Aachen"], departure=True) -> list:
    answer = input(f"Write {'a departure' if departure else 'an arrival'} cities in komma separated format or use default one: \n")
    if not answer or (answer == 'default'):
        return default
    else:
        return [city.strip().capitalize() for city in answer.split(",")]

    
def get_dates(dates: str) -> list[str]:
    if ',' in dates:
        dates = dates.split(',')
        dates = [i.strip() for i in dates]
    else:
        dates = [dates]

    result = []
    for date in dates:
        if '-' in date:
            date = date.split('-')
            date = [f"{i.strftime('%d.%m.%Y')}" for i in pd.date_range(start=date[0].strip(), end=date[1].strip())]
            result.extend(date)
        else:
            result.append(date)
    return result


if __name__ == "__main__":
    if input('Would you like to update data first?(y/n): ').lower() == 'y':
        ask_add_data()
    print()
    departure = ask_cities(departure=True)
    arrival = ask_cities(departure=False)
    uuids = get_uuids_from_db(departure, arrival)
    # dates_departure = [f"{0 if i < 10 else ''}{i}.08.2023" for i in range(1, 8)]
    dates_input = input("Write desirable dates komma separated or interval with dash: \n")
    dates_departure = get_dates(dates_input)
    
    trips = get_trips(
        departure_names=departure, 
        arrival_names=arrival, 
        dict_uuids=uuids,
        dates=dates_departure
      )
    
    trips = sorted(trips, key=lambda x: x[2], reverse=True)
    for trip in trips:
        print(trip[0: 7], end='\n\n')
 
