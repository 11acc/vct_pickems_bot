
# :: Scraping methods for matches

from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import tz
from dateutil.parser import parse

from .core import request_response
from db.db_instance import db
from db.queries import db_logic
from db.entity_classes import Match
from utils.bracket_assigner import compute_playoff_bracket_id


def convert_time(input_time: str) -> str:
    to_zone = tz.gettz('America/Scoresbysund')
    standard_time = input_time.astimezone(to_zone)
    return standard_time.strftime('%H:%M:%S')

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
        if not match_card:
            continue

        for a_tag_match in match_card.find_all('a', class_='wf-module-item'):
            skip_match = False
            team_ids = []
            winner_id = None

            team_divs = a_tag_match.find_all("div", class_="match-item-vs-team")
            if not team_divs:
                continue

            for team_div in team_divs:
                # Scrape team name
                text_div = team_div.find("div", class_="text-of")
                if text_div is None:  # If there's literally no text, default to "TBD"
                    team_name = "TBD"
                else:
                    # Get the scraped text
                    scraped_name = text_div.get_text(strip=True)
                    # If empty or “TBD”-like, store as "TBD"
                    team_name = scraped_name if scraped_name else "TBD"
                    if team_name.lower() in ("tbd", "tba"):
                        team_name = "TBD"

                team_id = db.get_team_id_by_name(team_name)
                if team_id is None:
                    print("No team detected, including TBD, skipping")
                    skip_match = True
                    break

                # Check if team is marked as the winner
                if "mod-winner" in team_div.get("class", []):
                    winner_id = team_id

                team_ids.append(team_id)

            # If no detected team, skip a_tag_match
            if skip_match:
                continue

            # Obtain time of match
            extracted_time = a_tag_match.find("div", class_="match-item-time").get_text(strip=True)
            try:
                time_obj = datetime.strptime(extracted_time, '%I:%M %p')
            except Exception as e:
                print(f"Failed to extract time [{extracted_time}] from match: {e}")
                continue

            # Convert time to deal with annoying matches overflowing days
            match_time = datetime.strftime(time_obj, '%H:%M:%S')
            time_parsed = parse(match_time)
            match_time = convert_time(time_parsed)

            # Obtain match bracket and kind
            match_type_raw = a_tag_match.find("div", class_="match-item-event").text.split("\n")
            match_type_split = [vlr_text.replace("\t", "") for vlr_text in match_type_raw if vlr_text]
            match_kind = match_type_split[0]
            match_bracket = match_type_split[1]

            # Obtain vlr match id
            match_href = a_tag_match.get("href", "")
            if not match_href:
                vlr_match_id = None
            else:
                # This assumes that the URL starts with a slash and the first segment is the vlr numeric id
                # For example, "/473233/..." -> vlr_match_id == "473233"
                vlr_match_id = match_href.split("/")[1]

            # Compute the playoffs bracket id
            m_playoff_bracket_id = compute_playoff_bracket_id(event_id, region, match_bracket, match_kind)

            # Create match class obj
            NewMatch = Match(
                None
                , team_ids[0]
                , team_ids[1]
                , winner_id
                , event_id
                , region
                , match_bracket
                , match_kind
                , match_date
                , match_time
                , vlr_match_id
                , m_playoff_bracket_id
            )

            # See if the match already exists in DB
            existing_match_id = db.get_match_from_vlr_match_id(NewMatch.vlr_match_id)
            ExistingMatch = db_logic.match_from_id(existing_match_id)

            if existing_match_id and ExistingMatch:
                # Update teams if they've changed
                if (ExistingMatch.team1_id != NewMatch.team1_id) or (ExistingMatch.team2_id != NewMatch.team2_id):
                    db.update_match_teams(existing_match_id, NewMatch.team1_id, NewMatch.team2_id)
                    print(f"Match id: {existing_match_id}, updating teams: {ExistingMatch.team1_id, ExistingMatch.team2_id} -> ({NewMatch.team1_id}, {NewMatch.team2_id})")

                # If the winner differs or is now known, update that too
                if (ExistingMatch.winner_id != NewMatch.winner_id and winner_id):
                    db.update_match_winner(existing_match_id, winner_id)
                    print(f"Match id: {existing_match_id}, adding winner: {winner_id}")

            else:
                # If no existing match, add the new one to the DB
                db.add_entry("matches", NewMatch)
                print(f"New match recorded: {NewMatch}")
