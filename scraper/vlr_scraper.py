
# :: Scraping methods for vlr.gg

import requests
from bs4 import BeautifulSoup
from datetime import datetime

from db.db_instance import db
from db.queries import db_logic
from db.entity_classes import Player, Points, BreakdownPts, Match, Vote


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
        player_id = db.get_player_id_from_vlr_name(player_name)
        PointsOfPlayer = db_logic.get_single_point_set(pt_player_id=player_id, pt_event_id=event_id)
        
        # If no point set, create a global points row
        if not PointsOfPlayer:
            print(f"No points set for: {player_name}, creating...")
            new_point_set = Points(None, player_id, event_id, 0)
            db.add_entry("points", new_point_set)
            # Re-fetch the points object after creation
            PointsOfPlayer = db_logic.get_single_point_set(pt_player_id=player_id, pt_event_id=event_id)
        
        # If no breakdown, create it
        if not PointsOfPlayer.breakdown:
            print(f"No breakdown pts set for: {player_name}, creating...")
            new_bd_set = BreakdownPts(None, PointsOfPlayer.point_id, player_points, player_vlr_id, region)
            db.add_entry("breakdown_pts", new_bd_set)

        # Check if they don't have the {region} breakdown
        has_region_bd = any(bd.region == region for bd in PointsOfPlayer.breakdown)
        # If not create it
        if not has_region_bd:
            print(f"No breakdown pts set for: {player_name} in region: {region}, creating...")
            new_bd_set = BreakdownPts(None, PointsOfPlayer.point_id, player_points, player_vlr_id, region)
            db.add_entry("breakdown_pts", new_bd_set)

        # Modify the specific breakdown points based on new scrapping
        PlayerBreakdownPts = db_logic.breakdown_from_points_n_region(PointsOfPlayer.point_id, region)
        db.modify_entry("breakdown_pts", "bd_nr_points", player_points, "breakdown_pts_id", PlayerBreakdownPts.breakdown_pts_id)

    # Update total point sets when done updating all players
    db_logic.update_total_point_sets()


def scrape_vlr_matches(event_id: int, region: str, url: str) -> None:
    response = request_response(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for date_tag in soup.find_all("div", class_="wf-label mod-large"):
        # Extract date first
        extracted_date = date_tag.find(text=True).strip()
        date_obj = datetime.strptime(extracted_date, '%a, %B %d, %Y')
        match_date = datetime.strftime(date_obj, '%Y-%m-%d')

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

                # Obtain time of match
                extracted_time = a_tag_match.find("div", class_="match-item-time").get_text(strip=True)
                time_obj = datetime.strptime(extracted_time, '%I:%M %p')
                match_time = datetime.strftime(time_obj, '%H:%M:%S')

                # Obtain match bracket and kind
                match_type_raw = a_tag_match.find("div", class_="match-item-event").text.split("\n")
                match_type_split = [vlr_text.replace("\t", "") for vlr_text in match_type_raw if vlr_text]
                match_kind = match_type_split[0]
                match_bracket = match_type_split[1]

                # Create match class obj & check if it already exists
                NewMatch = Match(None, *team_ids, winner_id, event_id, region, match_bracket, match_kind, match_date, match_time)

                # Check if match already exists but without a winner
                existing_match_id = db.get_match_without_winner(NewMatch)
                if existing_match_id:
                    if winner_id:
                        db.update_match_winner(existing_match_id, winner_id)
                        print(f"Updated match {existing_match_id} with winner {winner_id}")
                    # else:
                    #     print("Match exists in db with no winner change, skipping")
                    continue

                # Check if exact match (including winner) already exists
                if db.is_match_in_db(NewMatch):
                    # print("Match exists in db, with no change, skipping")
                    continue

                # Add to db
                db.add_entry("matches", NewMatch)


def scrape_vlr_votes(player_id: int, event_id: int, url: str) -> None:
    response = request_response(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for container in soup.find_all("div", class_="pickem-subseries-container"):
        # Extract bracket kind (title)
        bracket_kind = container.find('div', class_='wf-label mod-large').text.strip()
        match_bracket, match_kind = bracket_kind.split(":", 1)
        match_kind = match_kind.lstrip()
        
        # Find all match items in current container
        match_items = container.find_all('div', class_='wf-card pi-match-item noselect')

        for match in match_items:
            # Extract both team names from the container
            team_elements = match.find_all('div', class_='pi-match-item-team')
            team_full_names = [team_name.find('div', class_='pi-match-item-name').text.strip() for team_name in team_elements]
            team1_name = team_full_names[0]
            team2_name = team_full_names[1]

            # Note which team was selected from class property: .mod-selected
            selected_team = match.find('div', class_='mod-selected')
            if not selected_team:
                # print(f"No chosen team, skipping")
                continue
            chosen_team = selected_team.find('div', class_='pi-match-item-name').text.strip()
            chosen_team_id = db.get_team_id_from_name(chosen_team)

            # Identify match id from match info
            identified_match_id = db_logic.match_id_from_params(
                team1_id = db.get_team_id_from_name(team1_name)
                , team2_id = db.get_team_id_from_name(team2_name)
                , m_event_id = event_id
                , bracket = match_bracket
                , kind = match_kind
            )
            if not identified_match_id:
                print(f"Failed to identify match from extracted match information")
                continue

            # Construct Vote obj and save to DB
            NewVote = Vote(None, identified_match_id, chosen_team_id, player_id)

            # Check if vote already exists
            if db.is_vote_in_db(NewVote):
                # print("Vote exists in db, skipping")
                continue

            # Add to db
            db.add_entry("votes", NewVote)
