
import requests
from bs4 import BeautifulSoup

from database.redis_db import r
from database.db_utils import generate_event_key


def get_points_for_a_region(year, event, region, url):
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
        try:
            player_points = int(player_stats[0].split(" points")[0])
        except ValueError:
            print(f"Invalid points format: {player_stats[0]}")
            continue

        # Generate the appropriate key
        points_event_key = generate_event_key("points", year, event, region)
        metad_event_key = generate_event_key("metadata", year)

        # Store player: points in redis as zset
        r.zadd(points_event_key, {player_name: player_points})

        # Store metadata (like local) in a hset
        player_metadata_key = f"{metad_event_key}:player:{player_name}"
        r.hset(player_metadata_key, mapping={"local": player_local})
