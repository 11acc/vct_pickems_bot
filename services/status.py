
# :: Handle queries and formatting for discord command: status

from db.db_instance import db
from db.queries import db_logic
from utils.formatting import format_status_players
from utils.emojis import get_vct_emoji


# Currently ongoing event and players
def pickem_status() -> tuple[str, str] | None:
    ongoing_event_id = db_logic.ongoing_event_id()
    OngoingEvent = db_logic.event_from_id(ongoing_event_id)
    ongoing_title = f"{get_vct_emoji("kjcatdance")} Currently Ongoing Event: {get_vct_emoji(f"VCT {OngoingEvent.kind}")} {OngoingEvent.full_name}"

    # Player list with stars just like leaderboard service
    all_player_ids = db.get_all_player_ids()
    len_longest_name = 0
    PlayerStarCategoryCount = {}
    for p_id in all_player_ids:
        PlayerObj = db_logic.player_from_id(p_id)
        # For buffering
        name_length = len(PlayerObj.name)
        if name_length > len_longest_name:
            len_longest_name = name_length
        # Stars by player
        PlayerStarCategoryCount[PlayerObj], _ = db_logic.player_star_info(p_id)

    players_formatted = format_status_players(all_player_ids, len_longest_name, PlayerStarCategoryCount)

    return ongoing_title, players_formatted

