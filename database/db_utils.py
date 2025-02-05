
from database.redis_db import r
from bot.bot_utils import local_to_emoji, get_vct_emoji

# Redis get functions
def get_event_points(year: int, event_type: str):
    total_scores = {}
    breakdown = {}
    # Filter for region specific keys
    event_pattern = f"points:{year}:{event_type}:*"
    all_keys  = sorted(list(r.scan_iter(event_pattern)))

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

    # Add bet record


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


def generate_event_key(key_type: str, year: int, event=None, region=None) -> str:
    # Return with or without region depending on the type
    # of event_key necessary, for reference vlr_scrapper.py
    if key_type == "metadata":
        return f"{key_type}:{year}"
    else:
        return f"{key_type}:{year}:{event}:{region}"



# Styling functions
def loop_print_keys(r, list_of_keys):
    if not list_of_keys:
        return None
    
    pipe = r.pipeline()
    for key in list_of_keys:
        pipe.type(key)
    key_types = pipe.execute()

    key_operations = {
        'hash': lambda k: f"> {r.hgetall(k)}"
        , 'zset': lambda k: f"> {r.zrevrange(k, 0, -1, withscores=True)}"
    }

    for key, key_type in zip(list_of_keys, key_types):
        key_str = f"[{key}] ({key_type.upper()})"
        print(key_str)
        print(key_operations.get(key_type, lambda k: "")(key), "\n")


def print_keys(r):
    keys = r.keys("*")
    print(f"All Keys in Redis: {keys}\n")

    key_categories = {
        "/// METADATA ///": []
        , "/// POINTS ///": []
        , "/// BETS ///": []
        , "/// OTHER ///": []
    }
    for key in keys:
        if 'metadata:' in key:
            key_categories["/// METADATA ///"].append(key)
        elif 'points:' in key:
            key_categories["/// POINTS ///"].append(key)
        elif 'bets:' in key:
            key_categories["/// BETS ///"].append(key)
        else:
            key_categories["/// OTHER ///"].append(key)

    for category, keys in key_categories.items():
        if not keys:
            break
        print(category)
        loop_print_keys(r, keys)