
# :: Builds bracket configuration from event information

import os
import json

from db.db_instance import db
from db.queries import db_logic
from utils.bracket_id import get_bracket_id


def generate_bracket_config(event_id: int, region: str = None, year: str = None) -> dict:
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

    # Create custom identifier for generated bracket
    bracket_data["_id"] = get_bracket_id(event_id, region, year)

    for section in ["upper", "lower"]:
        for round_data in bracket_data[section]:
            for match in round_data["matches"]:
                # Find match through playoff id
                b_id = match["playoff_bracket_id"]
                if b_id in match_lookup:
                    match_obj = match_lookup[b_id]
                    # Team 1
                    match["team1"]["team_id"] = match_obj.team1_id
                    match["team1"]["name"] = match_obj.team1.short_name
                    match["team1"]["logo_url"] = match_obj.team1.logo_url
                    # Team 2
                    match["team2"]["team_id"] = match_obj.team2_id
                    match["team2"]["name"] = match_obj.team2.short_name
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
                    # Check tbd
                    match["tbd_check"] = False
                    if match_obj.team1_id == 404 or match_obj.team2_id == 404:
                        match["tbd_check"] = True
                    # Votes
                    votes_by_team_id = {team.team_id: players for team, players in match_obj.votes.items()}
                    if not votes_by_team_id:
                        print(f"No votes for match: {match}, skipping")
                        continue
                    for team_id, player in votes_by_team_id.items():
                        for p in player:
                            match_vote = {"player_id": p.player_id, "name": p.name, "icon_url": p.icon_url, "team_id": team_id}
                            if team_id == match_obj.team1_id:
                                match["votes_team1"].append(match_vote)
                            elif team_id == match_obj.team2_id:
                                match["votes_team2"].append(match_vote)
                            else:
                                match["votes_other"].append(match_vote)

    return bracket_data
