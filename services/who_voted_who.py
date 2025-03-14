
# :: Handle queries and formatting for discord command: who voted who

from datetime import datetime

from db.db_instance import db
from db.queries import db_logic
from utils.formatting import format_upcoming_match_votes


# Get information for who voted for which teams for the day's upcomming matches
def who_voted_who(next_param: int) -> str | None:
    # Format to ISO like in DB
    date_lookup = datetime.now().strftime('%Y-%m-%d')  # today

    # Get unfinished matches occurring today if next param is 0
    UpcomingMatches = db_logic.match_objs_for_date(date_lookup) if next_param == 0 else None

    # If no matches today find next unfinished upcoming matches or if next_param >0 skip n upcoming days
    if not UpcomingMatches:
        date_lookup = db.get_next_upcoming_match_date(date_lookup, next_param-1)  # -1 for intuitive use, 0 already goes to the next upcoming match
        UpcomingMatches = db_logic.match_objs_for_date(date_lookup) if date_lookup else None
        if not UpcomingMatches:
            print("No upcoming matches found")
            return None

    # Reformat date lookup
    format_date = datetime.strptime(date_lookup, '%Y-%m-%d')
    format_date = format_date.strftime('%a %B %d, %Y')

    return format_date, format_upcoming_match_votes(UpcomingMatches)