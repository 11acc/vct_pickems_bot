
# :: Methods to add/modify entries of the db through discord

from db.db_instance import db
from db.queries import db_logic
from db.entity_classes import Player, Star
from utils.emojis import format_local
from utils.event_assigner import star_tier_category


# Add new player to DB
def add_new_player(name: str, vlr_user: str, local: str, icon_url: str) -> bool:
    try:
        new_player = Player(None, name, vlr_user, local, icon_url)
        db.add_entry("players", new_player)
        return True
    except Exception as e:
        print(f"Something went wrong trying to add {new_player} to db: {str(e)}")
        return False

# Update player info
def update_player(existing_player_id: int, new_name: str = None, formatted_local: str = None, new_icon_url: str = None) -> bool:
    try:
        if new_name:
            db.modify_entry("players", "name", new_name, "player_id", existing_player_id)

        if formatted_local:
            db.modify_entry("players", "local", formatted_local, "player_id", existing_player_id)

        if new_icon_url:
            db.modify_entry("players", "icon_url", new_icon_url, "player_id", existing_player_id)

        return True

    except Exception as e:
        print(f"Error updating player with id {existing_player_id}: {str(e)}")
        return False

# Add new star to DB
def add_new_star(player_id: int, match_ev_id: int):
    try:
        category = f"{star_tier_category(match_ev_id)}_sparkle"
        new_star = Star(None, player_id, match_ev_id, category)
        db.add_entry("stars", new_star)
        return True

    except Exception as e:
        print(f"Something went wrong trying to add {new_star} to db: {str(e)}")
        return False
