
import requests
from bs4 import BeautifulSoup

from database.modules import db, Player, Points, BreakdownPts


def scrape_vlr_event_pickem(event_id: int, region: str, url: str) -> None:
    if url == "":
        print("Empty url, no event pickems for now, skipping")
        return None

    # Get html content for a url
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
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