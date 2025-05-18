
# :: Methods to add entries into the db through discord

from db.db_instance import db
from db.queries import db_logic
from db.entity_classes import Player, Star


# Add new player to DB
def add_new_player(name: str, vlr_user: str, local: str, icon_url: str) -> bool:
    try:
        new_player = Player(None, name, vlr_user, local, icon_url)
        db.add_entry("players", new_player)
        return True
    except Exception as e:
        print(f"Something went wrong trying to add {new_player} to db: {str(e)}")
        return False
