
# :: Core scraping utilities for vlr.gg

import requests


# Send a request to the given URL and return the response if successful
def request_response(url) -> str:
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None
    
    return response