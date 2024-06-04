def log(*msg: str) -> None:
    with open('trips.log', 'a') as file:
        file.write(' '.join(msg))
        file.write('\n')