
from database.sql_tables import get_points_from_event
from bot.bot_utils import local_to_emoji, get_vct_emoji


"""
!vct points kickoff 2025
    -> aggregate of 4 individual events
!vct points bangkok 2025
"""

def points_from_event(PointsFromEvent: list) -> str:
    # [(1, Alex, 5, 0, 'dcdde13e'), (2, Oliver, 5, 0, '8ba2e7a9'), (3, Qiff, 5, 0, 'dd6b6c9f')]
    # [(1, Alex, 5, {'americas': 0, }, '-'), ...]

    player_vars[player] = {
        "name": player
        , "local": r.hgetall(full_key)['local']
        , "total_points": total_points[player]
        , "breakdown_points": per_region.get(player, {})  # Get or empty dict if missing
    }

    pass


def format_player_info(year: int, event: str) -> list:
    # List of points and bets
    total_points, per_region = get_event_points(year, event)
    # bet_record = get_bet_record_event(year, event)

    # Redis key for metadata
    metad_event_key = generate_event_key("metadata", year)
    # Add player variables
    player_vars = {}
    for player in total_points.keys():
        # Filter for metadata data of each player
        full_key = metad_event_key + ":player:" + player
        player_vars[player] = {
            "name": player
            , "local": r.hgetall(full_key)['local']
            , "total_points": total_points[player]
            , "breakdown_points": per_region.get(player, {})  # Get or empty dict if missing
        }

    # Return formatting
    player_format = []
    longest_player_name = max(map(len, player_vars))  # for buffering
    for player_data in player_vars.values():
        
        breakdown_txt = " ".join(
            f"{get_vct_emoji(region)} `{points}`"
            for region, points in player_data['breakdown_points'].items()
        )
        # Calculate space buffer for each player
        buffer = longest_player_name - len(player_data['name']) + 3
        player_format.append(
            f"- {local_to_emoji(player_data['local'])} "
            f"`"
            f"{player_data['name']}"
            f"{" "*buffer}"
            f"{player_data['total_points']} points"
            f"`"
            f"  ( {breakdown_txt} "
            # f"{bet_record[player_data['name']]} )"
        )

    return player_format
