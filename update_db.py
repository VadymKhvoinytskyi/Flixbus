import sqlite3
from pathlib import Path

def add_initial_data():
    route = Path.cwd() / 'uuid_hash.db'
    con = sqlite3.connect(route)
    cur = con.cursor()

    uuids = {
            "Duesseldorf": "40d911c7-8646-11e6-9066-549f350fcb0c",
            "Cologne": "40d91025-8646-11e6-9066-549f350fcb0c", 
            "Moenchengladbach": "40da838e-8646-11e6-9066-549f350fcb0c",
            "Aachen": "40da8ddc-8646-11e6-9066-549f350fcb0c",
            "Paris": "40de8964-8646-11e6-9066-549f350fcb0c",
            "Amsterdam": "40dde3b8-8646-11e6-9066-549f350fcb0c",
            "Brussel": "40de6287-8646-11e6-9066-549f350fcb0c",
            "Barcelona": "40e086ed-8646-11e6-9066-549f350fcb0c",
            "Rotterdam": "40dee83e-8646-11e6-9066-549f350fcb0c",
            "Berlin": "40d8f682-8646-11e6-9066-549f350fcb0c",
            "Kyiv": "183cda51-3912-4707-95af-05238cd58ab8",
            "Luxembourg": "40da71d6-8646-11e6-9066-549f350fcb0c"
        }

    for key, value in uuids.items():
        cur.execute(f'INSERT INTO UUIDS VALUES ("{key}", "{value}");')
        
    con.commit()
    con.close()

add_initial_data()
