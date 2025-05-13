
# :: Builds bracket configuration from event information

import os
import json

from db.db_instance import db
from db.queries import db_logic


def generate_bracket_config(event_id: int, region: str = None) -> dict | None:
    # Find out which bracket type the event has
    bracket_type = db.get_bracket_type_from_event_id(event_id)
    if not bracket_type:
        print(f"No bracket type for event with id: {event_id}")

    # Use absolute path to templates directory
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    template_path = os.path.join(templates_dir, f"{bracket_type}.json")

    # Check if file exists
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found at: {template_path}")

    # Load the template
    with open(template_path, 'r', encoding='utf-8') as f:
        bracket_data = json.load(f)

    # Get all playoff matches for event
    match_data = db_logic.match_objs_for_playoffs(event_id, region)
    match_lookup = {match.playoff_bracket_id: match for match in match_data}

    for section in ["upper", "lower"]:
        for round_data in bracket_data[section]:
            for match in round_data["matches"]:
                # Find match through playoff id
                b_id = match["playoff_bracket_id"]
                if b_id in match_lookup:
                    match_obj = match_lookup[b_id]
                    # Team 1
                    match["team1"]["team_id"] = match_obj.team1_id
                    match["team1"]["name"] = match_obj.team1.name
                    match["team1"]["logo_url"] = match_obj.team1.logo_url
                    # Team 2
                    match["team2"]["team_id"] = match_obj.team2_id
                    match["team2"]["name"] = match_obj.team2.name
                    match["team2"]["logo_url"] = match_obj.team2.logo_url
                    # Winner
                    if match_obj.winner_id is not None:
                        match["winner"] = ("team1"
                                          if match_obj.winner_id == match_obj.team1_id
                                          else "team2"
                                          if match_obj.winner_id == match_obj.team2_id
                                          else "")
                    else:
                        match["winner"] = ""

    return bracket_data
