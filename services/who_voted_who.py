
# :: Handle queries and formatting for discord command: who voted who

from datetime import datetime

from db.db_instance import db
from db.queries import db_logic
from utils.formatting import format_upcoming_match_votes


# Get information for who voted for which teams for a set of upcomming matches
def who_voted_who(phase: str, region: str, skip_amount: int) -> tuple[str, str] | tuple[None, None]:
    # Format to ISO like in DB
    date_lookup = datetime.now().strftime('%Y-%m-%d')  # today
    # Normalise region
    region = region.capitalize()

    # Check if there's a match today
    match_id_lookup = db_logic.match_id_from_params(date=date_lookup)
    if not match_id_lookup:
        # If not, lookup next available match
        date_lookup = db.get_next_upcoming_match_date(date_lookup, region, skip_amount)
        match_id_lookup = db_logic.match_id_from_params(date=date_lookup, region=region)
        if not match_id_lookup:
            return None, None

    # The set of upcoming matches will vary if filtering by match kind (phase) or not
    format_date = UpcomingMatches = None

    if phase:
        match_kind = db.get_match_kind_from_id(match_id_lookup)
        if not match_kind:
            return None, None
        UpcomingMatches = db_logic.match_objs_for_week(match_kind, region)
        format_date = match_kind

    else:
        UpcomingMatches = db_logic.match_objs_for_date(date_lookup)
        # Reformat date lookup
        format_date = datetime.strptime(date_lookup, '%Y-%m-%d')
        format_date = format_date.strftime('%a %B %d, %Y')

    # Check if something happened or not
    if not UpcomingMatches:
        print("No upcoming matches found")
        return None, None

    return format_date, format_upcoming_match_votes(UpcomingMatches)


    # date_lookup = db.get_next_upcoming_match_date(date_lookup, next_param-1)  # -1 for intuitive use, 0 already goes to the next upcoming match
