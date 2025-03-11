
# :: Methods to match user input to propper db entry

from fuzzywuzzy import process

from db.db_instance import db


# Fuzzy match the user input event to the best match in the db
def find_best_event_match(input_event: str, year: int) -> str | None:
    events_in_year = db.get_events_in_year(year)
    if not events_in_year:
        return None
    all_event_names = [row for ev in events_in_year for row in ev if row]

    best_match, score = process.extractOne(input_event, all_event_names)
    if score >= 80:
        return best_match
    return None