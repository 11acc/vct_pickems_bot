
from fuzzywuzzy import process

from sql_tables import db
from reobot.bot_utils import local_to_emoji, get_vct_emoji


def tuple_into_class(class_table, sql_obj: tuple) -> any:
    return class_table(*sql_obj)

def find_best_event_match(input_event: str, year: int) -> any:
    events_in_year = db.fetch_all("SELECT loc FROM events WHERE year=?", (year,))
    all_event_names = [row for ev in events_in_year for row in ev if row]

    best_match, score = process.extractOne(input_event, all_event_names)
    if score >= 80:
        return best_match
    return None

def event_id_from_name(matched_name: str) -> int:
    pass

def point_sets_from_event_id(event_id: int) -> list:
    # c.execute("SELECT * FROM points WHERE pt_event_id=?", (2,))
    # list_of_things = c.fetchall()
    # PlayerPointsFromEvent = [tuple_into_class(Points, player_points) for player_points in list_of_things]
    # points_from_event(PlayerPointsFromEvent)
    pass

def points_from_event(matched_name: str) -> str | None:
    # Get all point sets for target event
    match_ev_id = event_id_from_name(matched_name)
    PlayerPointsFromEvent = point_sets_from_event_id(match_ev_id)

    points_formatted = []
    len_longest_name = max(len(p.player.name) for p in PlayerPointsFromEvent)  # for buffering
    for point_set in PlayerPointsFromEvent:
        # Breakdown of points if regional event
        breakdown_txt = (
            f" ( {' '.join(f'{get_vct_emoji(bd.region)} `{bd.bd_nr_points}`' for bd in point_set.breakdown)} ) "
            if len(point_set.breakdown) > 1
            else ""
        )
        # Calculate space buffer for each player
        buffer = len_longest_name - len(point_set.player.name) + 3
        points_formatted.append(
            f"- {local_to_emoji(point_set.player.local)} "
            f"`"
            f"{point_set.player.name}"
            f"{" "*buffer}"
            f"{point_set.nr_points} points"
            f"`"
            f"{breakdown_txt}"
        )

    return points_formatted
