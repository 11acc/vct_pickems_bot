
from database.redis_db import r
from bot.bot_utils import local_to_emoji, get_vct_emoji

# Redis get functions
def get_event_points(year: int, event_type: str):
    total_scores = {}
    breakdown = {}
    # Filter for region specific keys
    event_pattern = f"points:{year}:{event_type}:*"
    all_keys  = list(r.scan_iter(event_pattern))

    for region_key in all_keys:
        # Avoid erros for keys that slipped through filter and aren't zset
        key_type = r.type(region_key)
        if key_type != "zset":
            print(f"WARNING: {region_key} is not zset, it is a {key_type}. Skipping...")
            continue

        region_name = region_key.split(":")[-1]  # -1 -> region name (EMEA, AMER, ...)        
        players = r.zrevrange(region_key, 0, -1, withscores=True)

        for player, score in players:
            score = int(score)

            # Player total score            
            if player not in total_scores:
                total_scores[player] = 0
            total_scores[player] += score

            # Per region breakdown
            if player not in breakdown:
                breakdown[player] = {}
            breakdown[player][region_name] = score

    return total_scores, breakdown


def format_player_info(year: int, event: str):
    total_points, per_region = get_event_points(year, event.upper())
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
            f"  ( {breakdown_txt} )"
        )

    return player_format


def generate_event_key(key_type: str, year: int, event=None, region=None) -> str:
    # Return with or without region depending on the type
    # of event_key necessary, for reference vlr_scrapper.py
    if key_type == "metadata":
        return f"{key_type}:{year}"
    else:
        return f"{key_type}:{year}:{event}:{region}"



# Styling functions
def loop_print_keys(r, list_of_keys):
    for key in list_of_keys:
        key_type = r.type(key)

        if key_type == "hash":
            print(f"[{key}] (HASH)")
            print(f"> {r.hgetall(key)}\n")
        elif key_type == "zset":
            print(f"[{key}] (SORTED SET)")
            print(f"> {r.zrevrange(key, 0, -1, withscores=True)}\n")
        
        else:
            print(f"[{key}] (UNKNOWN)\n")


def print_keys(r):
    # Get all keys
    keys = r.keys("*")
    print(f"All Keys in Redis: {keys}\n")

    # Sort by event and type (metadata/points)
    metadata_keys = []
    point_keys = []
    for key in keys:
        if ':player:' in key:  # metadata
            metadata_keys.append(key)
        else:
            point_keys.append(key)

    print(f"/// METADATA ///")
    loop_print_keys(r, metadata_keys)
    print(f"/// POINTS ///")
    loop_print_keys(r, point_keys)