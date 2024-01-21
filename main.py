import requests
from pathlib import Path
import sqlite3
import pandas as pd
from datetime import datetime
from update_db import ask_add_data

def get_trips(departure_names: list[str], 
              arrival_names: list[str],  dict_uuids: dict[str: str], 
              dates: list[str]) -> list[dict]:
    
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
                    results_json = response.json()["trips"][0]["results"]

                    for key in results_json:
                        result_trips.append({
                            'departure': departure_name,
                            'arrival' : arrival_name,
                            'price' : results_json[key]['price']['average'],
                            'departure date' : results_json[key]['departure']['date'],
                            'arrival date' : results_json[key]['arrival']['date'],
                            'transfer type' : results_json[key]['transfer_type_key'],
                            'link' : f"https://shop.flixbus.ua/search?departureCity={departure_uuid}&arrivalCity={arrival_uuid}&rideDate={date}&adult=2&_locale=uk&features%5Bfeature.darken_page%5D=1&features%5Bfeature.enable_distribusion%5D=1&features%5Bfeature.train_cities_only%5D=0&features%5Bfeature.webc_search_persistent_explore_map%5D=0&atb_pdid=cc861ad2-ab97-43a7-971e-623e0c66e29f&_sp=1c858985-ce9b-4a8e-9e59-e4f41512f0b7&_spnuid=af71e384-6ff1-4a74-b031-8e7851f5e897"
                        })
    return result_trips


def get_uuids_from_db(
        departure_names: list[str], 
        arrival_names: list[str], 
        db_file = 'uuid_hash.db'
    ) -> dict[str: str]:
    cities = departure_names + arrival_names
    db_route = Path.cwd() / db_file
    con = sqlite3.connect(db_route)
    cur = con.cursor()
    res = cur.execute(f'SELECT City, UUID FROM UUIDS WHERE City in {tuple(cities)}')
    res = res.fetchall()
    con.commit()
    con.close()
    return dict(res)

def get_cities_from_str(answer: str, default: list=["Duesseldorf", "Moenchengladbach", "Cologne", "Aachen"]) -> list[str]:
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
