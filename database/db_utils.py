
# from reobot.bot_utils import local_to_emoji, get_vct_emoji(region)


def points_from_event(PlayerPointsFromEvent: list) -> str:
    points_formatted = []
    len_longest_name = max(len(p.player.name) for p in PlayerPointsFromEvent)  # for buffering
    for point_set in PlayerPointsFromEvent:
        # Breakdown of points if regional event
        breakdown_txt = (
            f" ( {' '.join(f'{bd.region} `{bd.bd_nr_points}`' for bd in point_set.breakdown)} ) "
            if len(point_set.breakdown) > 1
            else ""
        )
        # Calculate space buffer for each player
        buffer = len_longest_name - len(point_set.player.name) + 3
        points_formatted.append(
            f"- {point_set.player.local} "  # local_to_emoji(point_set.player.local)
            f"`"
            f"{point_set.player.name}"
            f"{" "*buffer}"
            f"{point_set.nr_points} points"
            f"`"
            f"{breakdown_txt}"
        )

    return points_formatted
