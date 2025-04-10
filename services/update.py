
# :: Handle scrapping for discord command: update

from db.db_instance import db
from db.queries import db_logic
from scraper.vlr_scraper import scrape_vlr_event_pickem, scrape_vlr_matches, scrape_vlr_votes


# Go to event's sub, and get all match urls, then scrape them all
def update_matches(event_id: int) -> None:
    event_match_region_urls = db_logic.subevent_region_match_urls_from_event_id(event_id)
    if not event_match_region_urls:
        return None

    for m_region, m_url in event_match_region_urls:
        scrape_vlr_matches(event_id, m_region, m_url)

# Go to event's sub, and get all pickem urls, then scrape them all
def update_pickem(event_id: int) -> None:
    event_pickem_region_urls = db_logic.subevent_region_pickem_urls_from_event_id(event_id)
    if not event_pickem_region_urls:
        return None

    for m_region, m_url in event_pickem_region_urls:
        scrape_vlr_event_pickem(event_id, m_region, m_url)

# Update all votes for a given event by going through existing point sets
def update_votes(event_id: int) -> None:
    # All points in event
    point_sets = db_logic.point_sets_from_filters(pt_event_id=event_id)

    for pt_set in point_sets:
        # Go to the breakdown pts
        for bd_set in pt_set.breakdown:
            # Construct vote url
            if not bd_set.vlr_handle:
                print(f"No vlr handle for bd_set: {bd_set.breakdown_pts_id}, skipping")
                continue
            url_to_scrape = f"https://www.vlr.gg/pickem/{bd_set.vlr_handle}"

            scrape_vlr_votes(pt_set.pt_player_id, event_id, url_to_scrape)


# Update on currently ongoing event
def update_current_pickems() -> None:
    curr_event_id = db_logic.ongoing_event_id()
    update_pickem(curr_event_id)

def update_current_matches() -> None:
    curr_event_id = db_logic.ongoing_event_id()
    update_matches(curr_event_id)

def update_current_votes() -> None:
    curr_event_id = db_logic.ongoing_event_id()
    update_votes(curr_event_id)

def update_all() -> None:
    curr_event_id = db_logic.ongoing_event_id()
    update_pickem(curr_event_id)
    update_matches(curr_event_id)
    update_votes(curr_event_id)