
import asyncio

from database.redis_db import r
from database.redis_db import check_redis_connection
# from scrapper.scheduler import start_scrapper
from scrapper.vlr_scrapper import get_points_for_a_region


async def main():
    # Ensure Redis is running
    if not check_redis_connection(r):
        print("Redis failed. Exiting...")
        return
    
    # Define which events will be tracked:
    events = [
        {"year": 2025, "event": "KICKOFF", "region": "EMEA", "url": "https://www.vlr.gg/event/leaderboard/2276/champions-tour-2025-emea-kickoff/?group=60e212d8"}
        , {"year": 2025, "event": "KICKOFF", "region": "AMERICAS", "url": "https://www.vlr.gg/event/leaderboard/2274/champions-tour-2025-americas-kickoff/?group=d651f69b"}
        , {"year": 2025, "event": "KICKOFF", "region": "PACIFIC", "url": "https://www.vlr.gg/event/leaderboard/2277/champions-tour-2025-pacific-kickoff/?group=770ba3c3"}
        , {"year": 2025, "event": "MASTERS", "region": "BANGKOK", "url": ""}
        , {"year": 2025, "event": "MASTERS", "region": "TORONTO", "url": ""}
        , {"year": 2025, "event": "CHAMPIONS", "region": "PARIS", "url": ""}
    ]

    #i11
    # for event in events:
    #     an_event = f"{event['year']} {event['event']} {event['region']}"
    #     try:
    #         print(f"Scraping {an_event} ...")
    #         get_points_for_a_region(event['year'], event['event'], event['region'], event['url'])
    #     except Exception as e:
    #         print(f"Error scrapping {an_event}: {e}")
    #i11


    # Run bot and periodic scrapper
    # await asyncio.gather(
    #     start_scrapper(events)
    #     , wakeup_reobot()
    # )



if __name__ == "__main__":
    asyncio.run(main())
