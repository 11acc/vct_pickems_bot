
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from database.modules import db, Player, Points, BreakdownPts, Match


def request_response(url) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None
    return response

def scrape_vlr_event_pickem(event_id: int, region: str, url: str) -> None:
    if url == "":
        print("Empty url, no event pickems for now, skipping")
        return None

    # Get html content for a url
    response = request_response(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    # Loop through each player row
    for player in soup.select('.event-container .event-content .wf-card a'):
        # Clean text and extract info
        player_stats = [line.strip() for line in player.text.splitlines() if line.strip()]

        player_name = player_stats[1]
        player_local = player_stats[2]
        player_vlr_id = str(player_stats[3].split("id: ")[1])
        try:
            player_points = int(player_stats[0].split(" points")[0])
        except ValueError:
            print(f"Invalid points format: {player_stats[0]}")
            continue

        # Check if player is in db, if not add them
        if not db.is_player_in_db(player_name):
            print(f"Player: {player_name} not in db, adding...")
            new_ply = Player(None, player_name, player_name, 0, player_local)
            db.add_entry("players", new_ply)
        
        # Obtain the point sets for the current player and event
        player_id = db.player_id_from_vlr_name(player_name)
        PointsOfPlayer = db.point_sets_from_filters(pt_player_id=player_id, pt_event_id=event_id)[0]
        
        # If no point set, create a global points row
        if not PointsOfPlayer:
            print(f"No points set for: {player_name}, creating...")
            new_point_set = Points(None, player_id, event_id, 0)
            db.add_entry("points", new_point_set)
        
        # If no breakdown, create it
        if not PointsOfPlayer.breakdown:
            print(f"No breakdown pts set for: {player_name}, creating...")
            new_bd_set = BreakdownPts(None, PointsOfPlayer.point_id, player_points, player_vlr_id, region)
            db.add_entry("breakdown_pts", new_bd_set)

        # Modify the specific breakdown points based on new scrapping
        PlayerBreakdownPts = db.breakdown_from_points_n_region(PointsOfPlayer.point_id, region)
        db.modify_entry("breakdown_pts", "bd_nr_points", player_points, "breakdown_pts_id", PlayerBreakdownPts.breakdown_pts_id)

    # Update total point sets when done updating all players
    db.update_total_point_sets()


def scrape_vlr_matches(event_id: int, url: str) -> None:
    response = request_response(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for date_tag in soup.find_all("div", class_="wf-label mod-large"):
        # Extract date first
        date_text = date_tag.find(text=True).strip()

        # Get the next sibling that is the match card
        match_card = date_tag.find_next_sibling('div', class_='wf-card')
        if match_card:
            for a_tag_match in match_card.find_all('a', class_='wf-module-item'):
                skip_match = False  # Flag in case of existing match in db or TBD matches
                team_ids = []
                winner_id = None

                for team in a_tag_match.find_all("div", class_="match-item-vs-team"):
                    # Scrape team name
                    text_div = team.find("div", class_="text-of")
                    if text_div is None:
                        print("No text detected, skipping")
                        skip_match = True
                        break
                    
                    team_name = text_div.get_text(strip=True)
                    team_id = db.get_team_id_by_name(team_name)
                    if team_id is None:
                        print("No team detected, skipping")
                        skip_match = True
                        break

                    if "mod-winner" in team.get("class", []):
                        winner_id = team_id
                    
                    team_ids.append(team_id)
                
                # If no detected team, skip a_tag_match
                if skip_match:
                    continue

                # Obtain time of match and join with date
                match_time = a_tag_match.find("div", class_="match-item-time").get_text(strip=True)
                match_datetime = datetime.strptime(date_text+", "+match_time, '%a, %B %d, %Y, %I:%M %p')
                match_date = match_datetime.strftime("%a, %B %d, %Y, %I:%M %p")

                # Obtain match bracket and kind
                match_type_raw = a_tag_match.find("div", class_="match-item-event").text.split("\n")
                match_type_split = [vlr_text.replace("\t", "") for vlr_text in match_type_raw if vlr_text]
                match_kind = match_type_split[0]
                match_bracket = match_type_split[1]

                # Create match class obj & check if it already exists
                new_match = Match(None, *team_ids, winner_id, event_id, match_bracket, match_kind, match_date)
                if db.check_match_in_db(new_match):
                    print("Match exists in db, skipping")
                    continue
                # Add to db
                db.add_entry("matches", new_match)
