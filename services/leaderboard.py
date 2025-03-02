
# :: Handle queries and formatting for discord command: leaderboard

from db.db_instance import db
from db.queries import db_logic
from utils.formatting import format_star_leaderboard


# Get star amount information for leading players
def star_leaderboard() -> str | None:
    player_ids_with_stars = db.get_player_ids_with_stars()
    # Define 2 dict by Player objs with respective star category counts and events
    PlayerStarCategoryCount = {}
    PlayerStarEvents = {}
    for p_id in player_ids_with_stars:
        PlayerObj = db_logic.player_from_id(p_id)
        PlayerStarCategoryCount[PlayerObj], PlayerStarEvents[PlayerObj] = db_logic.player_star_info(p_id)

    return format_star_leaderboard(PlayerStarCategoryCount, PlayerStarEvents)
