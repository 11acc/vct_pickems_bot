
# :: Methods to assign the proper star category to an event

from db.db_instance import db


def star_tier_category(match_ev_id: int) -> str | None:
    # Assign sparkle tier based on the kind of the event
    sparkle_tier = ""
    ev_kind = db.get_event_kind(match_ev_id)
    if ev_kind == "Champions":
        sparkle_tier = "champs"
    elif ev_kind == "Masters":
        sparkle_tier = "masters"
    elif ev_kind == "Champions Tour":
        sparkle_tier = "regular"
    else:
        print(f"Event kind not matching existing sparkles: {ev_kind}")
        return None
    return sparkle_tier

