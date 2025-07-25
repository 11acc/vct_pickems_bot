
# :: Methods to format ??

from collections import defaultdict

from .emojis import local_to_emoji, get_vct_emoji


# Format all player points for input event for the discord embed
def format_event_points(PlayerPointsFromEvent: list) -> str | None:
    REGION_ORDER = ["China", "Pacific", "Emea", "Americas"]

    # Find max name length and max points length per region in one pass
    len_longest_name = 0
    max_points_len_per_region = defaultdict(int)  # Region -> max length of points
    for point_set in PlayerPointsFromEvent:
        len_longest_name = max(len_longest_name, len(point_set.player.name))
        if len(point_set.breakdown) > 1:
            for bd in point_set.breakdown:
                points_str_len = len(str(bd.bd_nr_points))
                max_points_len_per_region[bd.region] = max(max_points_len_per_region[bd.region], points_str_len)

    # Format output
    points_formatted = []
    for point_set in PlayerPointsFromEvent:
        # Format breakdown with aligned points
        if len(point_set.breakdown) > 1:
            # Dict for quick lookup of points by region
            breakdown_dict = {bd.region: bd for bd in point_set.breakdown}
            # Build breakdown parts by the specified region order
            breakdown_parts = [
                f"{get_vct_emoji(region)} `{breakdown_dict[region].bd_nr_points:>{max_points_len_per_region[region]}}`"
                for region in REGION_ORDER
                if region in breakdown_dict
            ]
            breakdown_txt = f" ( {' '.join(breakdown_parts)} ) "
        else:
            breakdown_txt = ""

        # Calculate space buffer for player name
        buffer = len_longest_name - len(point_set.player.name) + 3

        points_formatted.append(
            f"- {local_to_emoji(point_set.player.local)} "
            f"`{point_set.player.name}{' ' * buffer}{point_set.nr_points} points`"
            f"{breakdown_txt}"
        )
    return points_formatted



# Formats star category counts into the appropriate vct emojis
def arrange_star_emojis(player_star_counts: dict) -> str:
    if not player_star_counts:
        return ''
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
            f"{get_vct_emoji(match.team1.name)} vs {get_vct_emoji(match.team2.name)}"
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

            team_line = f"  - {get_vct_emoji(team.name)}   {players_formatted}"
            formatted_matches.append(team_line)

        # Check if there are any non main team votes
        for phantom_team_id, phantom_players in votes_by_team_id.items():
            if phantom_team_id not in (match.team1_id, match.team2_id):
                # collect their names (with backticks)
                names = ", ".join(f"`{p.name}`" for p in phantom_players)
                # get the emoji for that phantom team
                emoji = get_vct_emoji(phantom_team_id)
                # append a single grouped line
                formatted_matches.append(
                    f"  - {names} actually thought {emoji} would get here..."
                )

        # Newline
        formatted_matches.append("")

    return "\n".join(formatted_matches).strip()



# Formatting for the status command, similar to leaderboard
def format_status_players(all_player_ids: list, len_longest_name: int, PlayerStarCategoryCount: list) -> str | None:
    status_formatted = [f"{get_vct_emoji("miku")} Players:"]
    for player in PlayerStarCategoryCount:
        buffer = len_longest_name - len(player.name)
        status_formatted.append(
            f"- {local_to_emoji(player.local)} "
            f"`"
            f"{player.name}"
            f"{" "*buffer}"
            f"`"
            f"  {arrange_star_emojis(PlayerStarCategoryCount[player])}"
        )
    return "\n".join(status_formatted)
