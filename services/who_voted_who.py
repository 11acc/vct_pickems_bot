
# :: Handle queries and formatting for discord command: who voted who

from datetime import datetime

from db.db_instance import db
from db.queries import db_logic
from utils.formatting import format_upcoming_match_votes


# [Day Format] Get information for who voted for which teams in a given day
def wvw_day(skip_amount: int) -> tuple[str, str] | tuple[None, None]:
    date_lookup = datetime.now().strftime('%Y-%m-%d')  # today

    # If user input skip, look for nth next upcoming match
    if skip_amount != 0:
        skip_amount -= 1  # for intuitive use
        date_lookup = db.get_next_upcoming_match_date(input_date=date_lookup, skipping_amount=skip_amount)

    # Check if there's a match for selected date
    match_id_lookup = db_logic.match_id_non_winner_from_params(date=date_lookup)
    if not match_id_lookup:
        date_lookup = db.get_next_upcoming_match_date(input_date=date_lookup, skipping_amount=skip_amount)
        match_id_lookup = db_logic.match_id_non_winner_from_params(date=date_lookup)
        if not match_id_lookup:
            return None, None

    UpcomingMatches = db_logic.match_objs_for_date(date_lookup)
    # Reformat date lookup
    format_date = datetime.strptime(date_lookup, '%Y-%m-%d')
    format_date = format_date.strftime('%a %B %d, %Y')

    if not UpcomingMatches:
        print("No upcoming matches found")
        return None, None

    return format_date, format_upcoming_match_votes(UpcomingMatches)


# Attempts to validate the provided date by checking for a match
def get_valid_match_date(date_lookup: str, region: str) -> str | None:
    # Check if there's a match on the given date
    if db_logic.match_id_non_winner_from_params(date=date_lookup, region=region):
        return date_lookup

    # Try to get the next upcoming match date
    new_date = db.get_next_upcoming_match_date(date_lookup, region=region, skipping_amount=0)
    if new_date and db_logic.match_id_non_winner_from_params(date=new_date, region=region):
        return new_date
    return None

# [Phase Format] Get information for who voted for which teams for a given phase (eg. Week 1)
def wvw_phase(region: str, skip_amount: int) -> tuple[str, str] | tuple[None, None]:
    date_lookup = datetime.now().strftime('%Y-%m-%d')  # today
    region = region.capitalize()

    # Validate the initial match date
    date_lookup = get_valid_match_date(date_lookup, region)
    if not date_lookup:
        return None, None

    # Get the match id and then the match kind
    match_id = db_logic.match_id_non_winner_from_params(date=date_lookup, region=region)
    match_kind = db.get_match_kind_from_id(match_id)
    if not match_kind:
        return None, None

    # If skipping is requested, move to the nth upcoming phase
    if skip_amount != 0:
        skip_amount -= 1  # for intuitive use
        date_lookup = db.get_next_upcoming_phase(date_lookup, region, skip_amount)
        # Re-validate the new date
        date_lookup = get_valid_match_date(date_lookup, region)
        if not date_lookup:
            return None, None
        match_id = db_logic.match_id_non_winner_from_params(date=date_lookup, region=region)
        match_kind = db.get_match_kind_from_id(match_id)
        if not match_kind:
            return None, None

    UpcomingMatches = db_logic.match_objs_for_week(match_kind, region)
    if not UpcomingMatches:
        print("No upcoming matches found")
        return None, None

    return match_kind, format_upcoming_match_votes(UpcomingMatches)


# Parent orchestrator method for Who Voted Who
def who_voted_who(region: str, skip_amount: int) -> tuple[str, str] | tuple[None, None]:
    # Normalise skip
    if not skip_amount:
        skip_amount = 0
    # If region, go to phase format
    if region:
        return wvw_phase(region, skip_amount)
    # If not default to day format
    return wvw_day(skip_amount)
