import sqlite3
import requests
from pathlib import Path

def add_data(uuids: dict[str: str]) -> None:
    route = Path.cwd() / 'uuid_hash.db'
    con = sqlite3.connect(route)
    cur = con.cursor()

    for key, value in uuids.items():
        try:
            cur.execute(f'INSERT INTO UUIDS VALUES ("{key}", "{value}");')
        except:
            pass
        
    con.commit()
    con.close()

user_input = input('Write country code(like UA) to download uuids.\n')
response = requests.get(
    'https://global.api.flixbus.com/cms/cities', 
    {'language': 'en', 'country': f'{user_input}'}
)
response_uuids = {res['slug'].capitalize(): res['uuid'] for res in response.json()['result']}
add_data(response_uuids)
print(f'Were added the following data: \n {response_uuids}')

