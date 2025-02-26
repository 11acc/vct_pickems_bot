
from fuzzywuzzy import process

from database.modules import db
from reobot.bot_utils import local_to_emoji, get_vct_emoji


# Fuzzy match the user input event to the best match in the db
def find_best_event_match(input_event: str, year: int) -> any:
    events_in_year = db.fetch_all("SELECT loc FROM events WHERE year=?", (year,))
    all_event_names = [row for ev in events_in_year for row in ev if row]

    best_match, score = process.extractOne(input_event, all_event_names)
    if score >= 80:
        return best_match
    return None

# Format all player points for input event for the discord embed
def points_from_event(matched_name: str) -> str | None:
    # Get event id and return the corresponding point sets associated
    match_ev_id = db.event_id_from_name(matched_name)
    PlayerPointsFromEvent = db.point_sets_from_filters(pt_event_id=match_ev_id)
    if not PlayerPointsFromEvent:
        return None
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

# Formats star category counts into the appropriate vct emojis
def format_star_emojis(player_star_counts: dict) -> str:
    emojis_formatted = []
    for category, count in player_star_counts.items():
        emojis_formatted.append(get_vct_emoji(f"{category}_{count}"))
    
    return ' '.join(emojis_formatted)

# Add bold or underline or both depending on event
def md_format_event_kind(AnEvent) -> str:
    md_prefix = md_suffix = ""
    bold = "**"
    underline = "__"

    if AnEvent.kind_tier == 1:
        md_prefix = bold + underline
        md_suffix = underline + bold
    elif AnEvent.kind_tier == 2:
        md_prefix = bold
        md_suffix = bold

    return f"{md_prefix}{AnEvent}{md_suffix}"

# Format events for star breakdown
def format_event_breakdown(player_star_events: list) -> str:
    return "\n".join(f"  - {md_format_event_kind(ev)}" for ev in player_star_events)

# Format the amount of stars and events won for players who have
def star_leaderboard() -> str | None:
    player_ids_with_stars = db.player_ids_with_stars()
    # Define 2 dict by Player objs with respective star category counts and events
    PlayerStarCategoryCount = {}
    PlayerStarEvents = {}
    for p_id in player_ids_with_stars:
        PlayerObj = db.get_player_by_id(p_id)
        PlayerStarCategoryCount[PlayerObj], PlayerStarEvents[PlayerObj] = db.get_player_star_info(p_id)

    # Format output
    stars_formatted = []
    for player in PlayerStarCategoryCount:
        stars_formatted.append(
            f"- {local_to_emoji(player.local)} "
            f" **{player.name}** "
            f"{format_star_emojis(PlayerStarCategoryCount[player])}"
            f"\n"
            f"{format_event_breakdown(PlayerStarEvents[player])}"
            f"\n"
        )

    return "\n".join(stars_formatted)
