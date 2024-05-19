-- look for all possible trips grouped by hour

with last_update as (
    SELECT max(downloaded_date)
    FROM Trips
), 
short_trips as (
    SELECT * 
    FROM Trips 
    WHERE transfer_number = 0 
        AND duration < 10
        AND downloaded_date in (SELECT * FROM last_update)
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
    (tt.departure || '-' || tt.arrival || '-' || tf.arrival),
    min(tt.price) + min(tf.price) as total_price,
    STRFTIME('%H, %d-%m-%Y', tt.departure_date) as dep_to,
    STRFTIME('%H, %d-%m-%Y', tt.arrival_date) as arr_to,
    STRFTIME('%H, %d-%m-%Y', tf.departure_date) as dep_from,
    STRFTIME('%H, %d-%m-%Y', tf.arrival_date) as arr_from
FROM trips_to tt
JOIN trips_from tf
ON tt.arrival = tf.departure
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



-- apply more filters to search and group by day

with last_update as (
    SELECT max(downloaded_date)
    FROM Trips
), 
filtered_trips as (
    SELECT * 
    FROM Trips 
    WHERE transfer_number <= 2
        AND duration < 20
        AND downloaded_date in (SELECT * FROM last_update)
),
default_cities (city) as (
    VALUES
    ("Duesseldorf"),
    ("Moenchengladbach"), 
    ("Cologne"), 
    ("Aachen")
),
desired_cities (city) as (
    VALUES
    ("Madrid"),
    ("Barcelona"), 
    ("London"), 
    ("Paris"),
    ("Stolholm"),
    ("Copenhagen"),
    ("Amsterdam")
),
trips_to as (
    SELECT * 
    FROM filtered_trips 
    WHERE departure in (
        SELECT * 
        FROM default_cities
    )
        AND price != 0
),
trips_from as (
    SELECT * 
    FROM filtered_trips 
    WHERE departure in (
        SELECT * 
        FROM desired_cities
    )
        AND price != 0
)
SELECT 
    (tt.departure || ' - ' || tt.arrival || ' - ' || tf.arrival) as route,
    min(tt.price) + min(tf.price) as total_price,
    STRFTIME('%d-%m-%Y', tt.departure_date) as dep_to,
    STRFTIME('%d-%m-%Y', tt.arrival_date) as arr_to,
    STRFTIME('%d-%m-%Y', tf.departure_date) as dep_from,
    STRFTIME('%d-%m-%Y', tf.arrival_date) as arr_from,
    julianday(tf.departure_date) - julianday(tt.arrival_date) as days_there
FROM trips_to tt
JOIN trips_from tf
ON tt.arrival = tf.departure
    AND tt.arrival_date < tf.departure_date
WHERE --cast(STRFTIME('%H', tt.departure_date) as decimal) in (7,8,9,10,11,12)
    cast(STRFTIME('%H', tt.arrival_date) as decimal) in (9,10,11,12,13,14,15,16,17,18)
    AND cast(STRFTIME('%H', tf.departure_date) as decimal) in (10,11,12,13,14,15,16,17,18)
    AND cast(STRFTIME('%H', tf.arrival_date) as decimal) in (6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,00)
    AND tt.arrival = "Amsterdam"
GROUP BY 
    tt.departure,
    tt.arrival,
    STRFTIME('%d-%m-%Y', tt.departure_date),
    STRFTIME('%d-%m-%Y', tt.arrival_date),
    STRFTIME('%d-%m-%Y', tf.departure_date),
    STRFTIME('%d-%m-%Y', tf.arrival_date)
HAVING julianday(tf.departure_date) - julianday(tt.arrival_date) >= 0.5
    AND julianday(tf.departure_date) - julianday(tt.arrival_date) <= 1
ORDER BY total_price
;
