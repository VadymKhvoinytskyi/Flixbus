-- database: c:\Programing\Python\Start_Python\flixbus\trips.db

-- Use the ▷ button in the top right corner to run the entire file.

with short_trips as (
    SELECT * 
    FROM Trips 
    WHERE transfer_number = 0 
        AND duration < 10
),
default_cities (city) as (
    VALUES
    ("Duesseldorf"),
    ("Moenchengladbach"), 
    ("Cologne"), 
    ("Aachen")
),
trips_to as (
    SELECT * 
    FROM short_trips 
    WHERE departure in (
        SELECT * 
        FROM default_cities
    )
),
trips_from as (
    SELECT * 
    FROM short_trips 
    WHERE departure not in (
        SELECT * 
        FROM default_cities
    )
)
SELECT 
    tt.departure,
    tt.arrival,
    min(tt.price) + min(tf.price) as total_price,
    STRFTIME('%H, %d-%m-%Y', tt.departure_date) as dep_to,
    STRFTIME('%H, %d-%m-%Y', tt.arrival_date) as arr_to,
    STRFTIME('%H, %d-%m-%Y', tf.departure_date) as dep_from,
    STRFTIME('%H, %d-%m-%Y', tf.arrival_date) as arr_from
FROM trips_to tt
JOIN trips_from tf
ON tt.departure = tf.arrival
    AND tt.arrival = tf.departure
    AND tt.arrival_date < tf.departure_date
WHERE cast(STRFTIME('%H', tt.departure_date) as decimal) in (6,7,8,9,10)
    AND cast(STRFTIME('%H', tf.arrival_date) as decimal) in (22,23,00,01)
GROUP BY 
    tt.departure,
    tt.arrival,
    STRFTIME('%H, %d-%m-%Y', tt.departure_date),
    STRFTIME('%H, %d-%m-%Y', tt.arrival_date),
    STRFTIME('%H, %d-%m-%Y', tf.departure_date),
    STRFTIME('%H, %d-%m-%Y', tf.arrival_date)
HAVING julianday(tf.departure_date) - julianday(tt.arrival_date) >= 0.5
ORDER BY total_price
;


/*SELECT 
    departure, 
    arrival, 
    STRFTIME('%H, %d-%m-%Y', departure_date) as hour_day_departure,
    min(price)
FROM short_trips
WHERE departure not in (SELECT * FROM default_cities)
GROUP BY 
    departure, 
    arrival, 
    STRFTIME('%H-%d-%m-%Y', departure_date)
;*/


