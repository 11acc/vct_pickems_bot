
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



# Generalised text effect method
def md_text_eff(input_str: str, text_eff: str) -> str | None:
    if text_eff != "bold" and text_eff != "underline" and text_eff != "bold underline":
        print(f"Unrecognised text effect: {text_eff}")
        return None

    md_prefix = md_suffix = ""
    bold = "**"
    underline = "__"

    if text_eff == "bold underline":
        md_prefix = bold + underline
        md_suffix = underline + bold
    elif text_eff == "bold":
        md_prefix = bold
        md_suffix = bold
    elif text_eff == "bold":
        md_prefix = underline
        md_suffix = underline

    return f"{md_prefix}{input_str}{md_suffix}"

# Format upcoming matches by categorising player votes by teams
def format_upcoming_match_votes(UpcomingMatches: list) -> str | None:
    formatted_matches = []
    
    for match in UpcomingMatches:
        # Create block header
        match_title = f"{match.bracket}: {match.kind}  ·"
        header_line = (
            f"- {get_vct_emoji(match.region)} "
            f"{md_text_eff(match_title, 'bold')}  "
            f"{get_vct_emoji(match.team1.short_name)} vs {get_vct_emoji(match.team2.short_name)}"
        )
        formatted_matches.append(header_line)

        # Build a new dictionary from match.votes to not care about team order
        votes_by_team_id = {team.team_id: players for team, players in match.votes.items()}

        # For each team, format the votes
        for team in (match.team1, match.team2):
            all_players = votes_by_team_id.get(team.team_id, [])
            if all_players:
                players_formatted = " ".join(f"`{player.name}`" for player in all_players)
            else:
                players_formatted = "`—`"
            team_line = f"  - {get_vct_emoji(team.short_name)}   {players_formatted}"
            formatted_matches.append(team_line)
        
        # Newline
        formatted_matches.append("")

    return "\n".join(formatted_matches).strip()
