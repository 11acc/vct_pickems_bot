
# :: Handle queries and formatting for discord command: who voted who

from datetime import datetime

from db.db_instance import db
from db.queries import db_logic
from utils.formatting import format_upcoming_match_votes


# Get information for who voted for which teams for the day's upcomming matches
def who_voted_who(next_param: int) -> str | None:
    # If next param is 0 default to today, if >0 skip n upcoming days

    # Format to ISO like in DB
    today = datetime.now().strftime("%Y-%m-%d")
    # today = "2025-03-23"

    # Get matches occurring today
    UpcomingMatches = db_logic.match_objs_for_date(today)

    # If no matches today, find next upcoming matches
    if not UpcomingMatches:
        next_date = db.get_next_upcoming_match_date(today)
        UpcomingMatches = db_logic.match_objs_for_date(next_date) if next_date else None
        if not UpcomingMatches:
            print("No upcoming matches found")
            return None

    return format_upcoming_match_votes(UpcomingMatches)