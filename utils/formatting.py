
# :: Methods to format ??

from .emojis import local_to_emoji, get_vct_emoji


# Format all player points for input event for the discord embed
def format_event_points(PlayerPointsFromEvent: list) -> str | None:
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
def arrange_star_emojis(player_star_counts: dict) -> str:
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
def arrange_event_breakdown(player_star_events: list) -> str:
    return "\n".join(f"  - {md_format_event_kind(ev)}" for ev in player_star_events)

# Format the amount of stars and events won for players who have
def format_star_leaderboard(PlayerStarCategoryCount: list, PlayerStarEvents: list) -> str | None:
    # Format output
    stars_formatted = []
    for player in PlayerStarCategoryCount:
        stars_formatted.append(
            f"- {local_to_emoji(player.local)} "
            f" **{player.name}** "
            f"{arrange_star_emojis(PlayerStarCategoryCount[player])}"
            f"\n"
            f"{arrange_event_breakdown(PlayerStarEvents[player])}"
            f"\n"
        )
    return "\n".join(stars_formatted)


# Format x
"""
    desc = 
- **Swiss Stage: Round 1  ·**  {get_vct_emoji('vit')} vs {get_vct_emoji('t1')}
  - {get_vct_emoji('vit')}   `Alex`  `Ting`
  - {get_vct_emoji('t1')}   `Qiff`  `Oliver`  `Maka`
- **Swiss Stage: Round 1  ·**  {get_vct_emoji('g2')} vs {get_vct_emoji('te')}
  - {get_vct_emoji('g2')}   `Alex`  `Ting`  `Qiff`
  - {get_vct_emoji('te')}   `Oliver`  `Maka`
  
    embed.set_image(url="https://i.ytimg.com/vi/FA3f5TGNj7s/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBt2kHJKriLP0D5XXptHurNnd7a1Q")
    embed.set_footer(
        text="Fri, February 21, 2025"
    )
"""