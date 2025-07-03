
# :: Core scraping utilities for vlr.gg

import requests


# Send a request to the given URL and return the response if successful
def request_response(url) -> str | None:
    try:
        response = requests.get(url)
    except Exception as e:
        return None

    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None

    return response
