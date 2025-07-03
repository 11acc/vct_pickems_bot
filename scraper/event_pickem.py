
# :: Scraping methods for event pickems

from bs4 import BeautifulSoup

from .core import request_response
from db.db_instance import db
from db.queries import db_logic
from db.entity_classes import Player, Points, BreakdownPts


def scrape_vlr_event_pickem(event_id: int, region: str, url: str) -> None:
    if url == "":
        print("Empty url, no event pickems for now, skipping")
        return None

    response = request_response(url)
    if response is None:
        print(f"[scrape_vlr_pickems] There was an error with input url: {url}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Loop through each player row
    for player in soup.select('.event-container .event-content .wf-card a'):
        # Clean text and extract info
        player_stats = [line.strip() for line in player.text.splitlines() if line.strip()]

        player_name = player_stats[1]
        player_local = player_stats[2]
        player_vlr_id = str(player_stats[3].split("id: ")[1])
        try:
            player_points = int(player_stats[0].split(" pts")[0])
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
