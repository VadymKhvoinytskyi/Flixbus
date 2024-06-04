import click
from datetime import datetime
# from update_db import ask_add_data
from main import get_trips, get_cities_from_str, get_dates # , get_uuids_from_db
from utils import log

@click.command()
@click.option('--departure', default='', help='comma separated departure cities')
@click.option('--arrival', default='', help='comma separated arrival cities')
@click.option('--dates', help='comma or/and dash separated dates')
@click.option('--link', default=False, help='whether or not show link')
def main(departure: str, arrival: str, dates: str, link: bool) -> None:
    log(f"Inputs: departure {departure}, arrival {arrival}, dates {dates}")

    departure: list = get_cities_from_str(departure)
    arrival: list = get_cities_from_str(arrival)
    dates_departure: list = get_dates(dates)

    log(f"Processed inputs: departure {departure}, arrival {arrival}, dates_departure {dates_departure}")

    trips = get_trips(
        departure_names=departure, 
        arrival_names=arrival,
        dates=dates_departure,
        verbose=True
    )

    log(f"Number of trips is {len(trips)}")

    trips = sorted(trips, key=lambda x: x['price'], reverse=True)
    for trip in trips:
        if link:
            click.echo(list(trip.values())[0:7])
            click.echo('\n')
        else:
            trips = list(trip.values())[0:6]
            duration = datetime.fromisoformat(trips[4]) - datetime.fromisoformat(trips[3])
            click.echo(trips + [round(duration.days * 24 + duration.seconds / 3600, 2)])
            click.echo('\n')

if __name__ == "__main__":
    # if input('Would you like to update data first?(y/n): ').lower() == 'y':
    #     ask_add_data()
    # print('\n')

    main()

    
