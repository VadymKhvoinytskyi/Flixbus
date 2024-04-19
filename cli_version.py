import click
# from update_db import ask_add_data
from main import get_trips, get_cities_from_str, get_dates # , get_uuids_from_db

@click.command()
@click.option('--departure', default='', help='comma separated departure cities')
@click.option('--arrival', default='', help='comma separated arrival cities')
@click.option('--dates', help='comma or/and dash separated dates')
@click.option('--link', default=False, help='whether or not show link')
def main(departure: str, arrival: str, dates: str, link: bool) -> None:
    departure: list = get_cities_from_str(departure)
    arrival: list = get_cities_from_str(arrival)
    dates_departure: list = get_dates(dates)

    trips = get_trips(
        departure_names=departure, 
        arrival_names=arrival,
        dates=dates_departure,
        verbose=True
    )

    trips = sorted(trips, key=lambda x: x['price'], reverse=True)
    for trip in trips:
        if link:
            click.echo(list(trip.values())[0:7])
            click.echo('\n')
        else:
            click.echo(list(trip.values())[0:6])
            click.echo('\n')

if __name__ == "__main__":
    # if input('Would you like to update data first?(y/n): ').lower() == 'y':
    #     ask_add_data()
    # print('\n')

    main()

    
