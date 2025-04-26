
# :: Scraping methods for votes

from bs4 import BeautifulSoup

from .core import request_response
from db.db_instance import db
from db.queries import db_logic
from db.entity_classes import Vote


def scrape_vlr_bracket_votes(soup, player_id: int, event_id: int, region: str) -> None:
    # Find all match spans. Each match is represented by a <span> with class "bracket-item" and "mod-pickem"
    for match_span in soup.find_all("span", class_=lambda x: x and "bracket-item" in x and "mod-pickem" in x):
        skip_match = False  # Flag in case of existing match in db or TBD matches
        team_ids = []
        chosen_team_id = None

        # Get the two teams; they are in divs with class "bracket-item-team"
        team_divs = match_span.find_all("div", class_="bracket-item-team")
        for team_div in team_divs:
            team_name_elem = team_div.find("div", class_="bracket-item-team-name")
            team_name = team_name_elem.find("span").get_text(strip=True) if team_name_elem else ""
            if team_name is None:
                print("No text detected, skipping")
                skip_match = True
                break

            team_id = db.get_team_id_from_name(team_name)
            if team_id is None:
                print("No team detected, skipping")
                skip_match = True
                break

            # Determine the chosen team for this match
            if "mod-selected" in team_div.get("class", []):
                chosen_team_id = team_id

            team_ids.append(team_id)

        # Check if we got a chosen team id
        if not chosen_team_id:
            print(f"No winner selected, no votes, exiting")
            skip_match = True
            break

        # If no detected team, skip a_tag_match
        if skip_match:
            continue

        # Get the bracket "kind" from the parent column label.
        col_div = match_span.find_parent("div", class_=lambda x: x and "bracket-col" in x)
        match_kind = ""
        if col_div:
            label_div = col_div.find("div", class_="bracket-col-label")
            if label_div:
                match_kind = label_div.get_text(strip=True)

        # In the pickem-bracket-container all matches are from the Playoffs bracket
        match_bracket = "Playoffs"
        # match_kind = "Upper Round 1"  # fuck u vlr why don't you have this text on the bracket

        # Extract the playoff bracket id from the span’s data attribute
        playoff_bracket_id = match_span.get("data-curr-id")
        if not playoff_bracket_id:
            print("No data-curr-id found, skipping")
            continue

        # Identify match id from match info
        identified_match_id = db_logic.match_id_from_params(
            m_event_id = event_id
            , region = region
            , bracket = match_bracket
            , kind = match_kind
            , playoff_bracket_id = playoff_bracket_id
        )
        if not identified_match_id:
            # print(f"Failed to identify match from extracted match information - playoff_bracket_id, match_kind: {playoff_bracket_id}, {match_kind}")
            continue

        # Construct Vote obj
        NewVote = Vote(None, identified_match_id, chosen_team_id, player_id)

        # Check if vote already exists
        existing_vote_id = db.get_vote_id_without_voted_team(NewVote)
        voted_team_id = db.get_team_id_from_vote(existing_vote_id)
        if existing_vote_id:
            # If the team choice has changed, update the vote in the DB
            if voted_team_id != chosen_team_id:
                db.update_vote_choice(existing_vote_id, chosen_team_id)
                print(f"Vote id: {existing_vote_id}, updating choice: {existing_vote_id} -> ({chosen_team_id}")
        else:
            # Vote doesn't exist, insert it.
            db.add_entry("votes", NewVote)
            print(f"New votes recorded: {NewVote}")

def scrape_vlr_subseries_votes(soup, player_id: int, event_id: int) -> None:
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
                # print(f"Failed to identify match from extracted match information")
                continue

            # Construct Vote obj
            NewVote = Vote(None, identified_match_id, chosen_team_id, player_id)

            # Check if vote already exists
            existing_vote_id = db.get_vote_id_without_voted_team(NewVote)
            voted_team_id = db.get_team_id_from_vote(existing_vote_id)
            
            if existing_vote_id:
                # If the team choice has changed, update the vote in the DB
                if voted_team_id != chosen_team_id:
                    db.update_vote_choice(existing_vote_id, chosen_team_id)
                    print(f"Vote id: {existing_vote_id}, updating choice: {existing_vote_id} -> ({chosen_team_id}")
            else:
                # Vote doesn't exist, insert it.
                db.add_entry("votes", NewVote)
                print(f"New votes recorded: {NewVote}")

def scrape_vlr_votes(player_id: int, event_id: int, region: str, url: str) -> None:
    response = request_response(url)
    if response is None:
        return None
    soup = BeautifulSoup(response.content, "html.parser")

    # Scrape bracket (playoffs)
    bracket_html = soup.find_all("div", class_="pickem-bracket-container")
    if bracket_html:
        scrape_vlr_bracket_votes(soup, player_id, event_id, region)

    # Scrape subseries (group stage)
    subseries_html = soup.find_all("div", class_="pickem-subseries-container")
    if subseries_html:
        scrape_vlr_subseries_votes(soup, player_id, event_id)

