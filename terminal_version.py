import requests
from pathlib import Path
import sqlite3
import pandas as pd
from datetime import datetime
from update_db import ask_add_data
from main import get_trips, get_uuids_from_db, get_cities_from_str, get_dates


if __name__ == "__main__":
    if input('Would you like to update data first?(y/n): ').lower() == 'y':
        ask_add_data()
    print('\n')

    departure = get_cities_from_str(
        input(
            f"Write a departure cities in comma separated format or use default one: \n"
        )
    )
    arrival = get_cities_from_str(
        input(
            f"Write an arrival cities in comma separated format or use default one: \n"
        )
    )

    uuids = get_uuids_from_db(departure, arrival)
    dates_input = input("Write desirable dates comma separated or interval with dash: \n")
    dates_departure = get_dates(dates_input)
    
    trips = get_trips(
        departure_names=departure, 
        arrival_names=arrival, 
        dict_uuids=uuids,
        dates=dates_departure
    )
    
    trips = sorted(trips, key=lambda x: x['price'], reverse=True)
    for trip in trips:
        print(list(trip.values())[0:6], end='\n\n')
 
    # TODO: store output in database
    # TODO: get weather
