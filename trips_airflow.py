import json
from datetime import datetime

import pandas as pd

# from update_db import ask_add_data
from main import get_trips, get_dates # , get_uuids_from_db, get_cities_from_str 

def dates_validation(dates) -> list:
    if not dates:
        return [datetime.today().strftime('%d.%m.%Y')]
    elif isinstance(dates, str):
        return get_dates(dates)
    elif isinstance(dates, list):
        return dates
    else:
        raise ValueError('Wrong value for dates provided!')

def download_trips(
    departure: list=None, 
    arrival: list=None, 
    dates: list=None, 
    link: bool=True
) -> None:

    with open('trips_config.json', 'r') as file:
        config = json.load(file)
        departure: list = config['departure'] if not departure else departure
        arrival: list = config['arrival'] if not arrival else arrival
    
    dates_departure = dates_validation(dates)

    trips_to = get_trips(
        departure_names=departure, 
        arrival_names=arrival,
        dates=dates_departure
    )

    trips_from = get_trips(
        departure_names=arrival, 
        arrival_names=departure,
        dates=dates_departure
    )

    trips_all = trips_to + trips_from

    with open('latest.csv', 'a') as file:
        # trip = trips_all[0]
        # trip_line = str(list(trip.keys()))[1:-1].replace("'", '')
        # file.write(f'{trip_line}\n')
        for trip in trips_all:
            trip_line = str(list(trip.values()))[1:-1].replace("'", '')
            file.write(f'{trip_line}\n')

def number_of_parts(string: str, sep: str='#') -> int:
    return len(string.split(sep))

def calculate_duration(dates) -> int:
    return (pd.to_datetime(dates['arrival date']) - pd.to_datetime(dates['departure date'])).total_seconds() / (60 * 60)

def create_calculated_fields(file_name: str='latest.csv') -> None:
    df = pd.read_csv(file_name, sep=', ', engine='python')

    df['transfer_number'] = df['transfer type'].apply(lambda x: number_of_parts(x)-1)
    df['duration'] = df[['departure date', 'arrival date']].apply(calculate_duration, axis=1)
    df['downloaded_date'] = datetime.today().strftime('%d.%m.%Y')

    df.to_csv(file_name.split('.')[0] + '_enriched.csv', index=False)

# download_trips()

create_calculated_fields()