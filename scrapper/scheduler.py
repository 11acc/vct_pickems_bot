
import asyncio
import logging
from scrapper.vlr_scrapper import get_points_for_a_region


async def scrape_loop(events):
    while True:
        logging.info("running scrapper...")

        for event in events:
            try:
                logging.info(f"Scraping {event['event_key']}...")
                get_points_for_a_region(event['event_key'], event['url'])
            except Exception as e:
                logging.error(f"Error scrapping {event['event_key']}: {e}")

        logging.info("Next scrape in a day...")
        await asyncio.sleep(86400)  # every day

async def start_scrapper(events):
    asyncio.create_task(scrape_loop(events))
