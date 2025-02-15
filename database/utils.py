
# from reobot.bot_utils import local_to_emoji


def points_from_event(PointsInEvent: list) -> str:
    """
        PointSetList = [
            [Kazakhstan Alex, 0 points, event id: 5]
            , [Afghanistan Oliver, 0 points, event id: 5]
            , [Hong Kong Qiff, 0 points, event id: 5]
        ]

        PointSetList = [
            [Kazakhstan Alex, 55+ points, event ids: 1,2,4,6]
        ]

    """

    # Return formatting
    points_formatted = []
    len_longest_name = max(len(p.player.name) for p in PointsInEvent)  # for buffering
    for point_set in PointsInEvent:
        # breakdown?
        # Calculate space buffer for each player
        buffer = len_longest_name - len(point_set.player.name) + 3
        points_formatted.append(
            f"- {point_set.player.local} "  # local_to_emoji(point_set.player.local)
            f"`"
            f"{point_set.player.name}"
            f"{" "*buffer}"
            f"{point_set.nr_points} points"
            f"`"
            # f"  ( {breakdown_txt} )"
        )

    return points_formatted
        # breakdown_txt = " ".join(
        #     f"{get_vct_emoji(region)} `{points}`"
        #     for region, points in player_data['breakdown_points'].items()
        # )


# def format_player_info(year: int, event: str) -> list:
#     # List of points and bets
#     total_points, per_region = get_event_points(year, event)
#     # bet_record = get_bet_record_event(year, event)

#     # Redis key for metadata
#     metad_event_key = generate_event_key("metadata", year)
#     # Add player variables
#     player_vars = {}
#     for player in total_points.keys():
#         # Filter for metadata data of each player
#         full_key = metad_event_key + ":player:" + player
#         player_vars[player] = {
#             "name": player
#             , "local": r.hgetall(full_key)['local']
#             , "total_points": total_points[player]
#             , "breakdown_points": per_region.get(player, {})  # Get or empty dict if missing
#         }

#     # Return formatting
#     player_format = []
#     longest_player_name = max(map(len, player_vars))  # for buffering
#     for player_data in player_vars.values():
        
#         breakdown_txt = " ".join(
#             f"{get_vct_emoji(region)} `{points}`"
#             for region, points in player_data['breakdown_points'].items()
#         )
#         # Calculate space buffer for each player
#         buffer = longest_player_name - len(player_data['name']) + 3
#         player_format.append(
#             f"- {local_to_emoji(player_data['local'])} "
#             f"`"
#             f"{player_data['name']}"
#             f"{" "*buffer}"
#             f"{player_data['total_points']} points"
#             f"`"
#             f"  ( {breakdown_txt} "
#             # f"{bet_record[player_data['name']]} )"
#         )

