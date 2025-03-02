
# :: Handle queries and formatting for discord command: points from event

from db.db_instance import db
from db.queries import db_logic
from utils.formatting import format_event_points


# Get event id from matched name and return the corresponding point sets associated
def points_from_event(matched_name: str) -> list | None:
    match_ev_id = db.get_event_id_from_name(matched_name)
    PlayerPointsFromEvent = db_logic.point_sets_from_filters(pt_event_id=match_ev_id)
    if not PlayerPointsFromEvent:
        return None
    # Format points for discord embed
    return format_event_points(PlayerPointsFromEvent)