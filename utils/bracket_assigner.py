
# :: Methods to assign the proper match playoff_bracket_ids

from db.db_instance import db


PLAYOFF_CONFIGS = {
    "8d22": {
        "Upper Round 1":       ["111", "121"],
        "Upper Semifinals":    ["211", "221"],
        "Upper Final":         "311",
        "Grand Final":         "411",
        "Lower Round 1":       ["112", "122"],
        "Lower Round 2":       ["222", "212"],
        "Lower Round 3":       "312",
        "Lower Final":         "412",
    },
    "8d00": {
        "Upper Quarterfinals": ["121", "111", "131", "141"],
        "Upper Semifinals":    ["211", "221"],
        "Upper Final":         "311",
        "Grand Final":         "411",
        "Lower Round 1":       ["112", "122"],
        "Lower Round 2":       ["222", "212"],
        "Lower Round 3":       "312",
        "Lower Final":         "412",
    },
    # add more event-level bracket_type entries here...
}

# Returns the appropriate playoff_bracket_id (e.g. "111", "121", etc.) for a given match
def compute_playoff_bracket_id(event_id: int, match_region: str, match_bracket: str, match_kind: str) -> str | None:
    if match_bracket != "Playoffs":
        # print(f"computing brackt id FAIL > bracket type not playoffs: {match_bracket}")
        return None

    # 1) Fetch the event's bracket_type
    bracket_type = db.get_bracket_type_from_event_id(event_id)

    # 2) Lookup that config
    cfg = PLAYOFF_CONFIGS.get(bracket_type)
    if not cfg:
        # print(f"computing brackt id FAIL > no config: {cfg}")
        return None

    kind_map = cfg.get(match_kind)
    if kind_map is None:
        # print(f"computing brackt id FAIL > no config kind mapped: {match_kind}")
        return None

    # 3) If it's a single id, return it
    if isinstance(kind_map, str):
        return kind_map

    # 4) It's a list → count how many we already have
    count_row = db.fetch_one(
        """
        SELECT COUNT(*) 
          FROM matches
         WHERE m_event_id=?
           AND region=?
           AND bracket='Playoffs'
           AND kind=?
        """,
        (event_id, match_region, match_kind)
    )
    already = count_row[0] if count_row else 0

    # pick the next index in the list
    if already < len(kind_map):
        return kind_map[already]
    else:
        # more matches inserted than expected...
        # print(f"computing brackt id FAIL > We already have matches of type: {match_bracket} {match_kind} for event {event_id} in region {match_region}")
        return None
