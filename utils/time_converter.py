
# :: Methods to convert scraped time a consistent format and timezone of the event's region

from dateutil import tz


CITY_TIMEZONES = {
    'reykjavik': 'Atlantic/Reykjavik',
    'berlin': 'Europe/Berlin',
    'copenhagen': 'Europe/Copenhagen',
    'istanbul': 'Europe/Istanbul',
    'sao paulo': 'America/Sao_Paulo',
    'tokyo': 'Asia/Tokyo',
    'los angeles': 'America/Los_Angeles',
    'madrid': 'Europe/Madrid',
    'shanghai': 'Asia/Shanghai',
    'seoul': 'Asia/Seoul',
    'bangkok': 'Asia/Bangkok',
    'toronto': 'America/Toronto',
    'paris': 'Europe/Paris',

    'glasgow': 'Europe/London',  # its coming 100% trust!!
    'new york': 'America/New_York',
    'chicago': 'America/Chicago',
    'detroit': 'America/Detroit',
    'london': 'Europe/London',
    'barcelona': 'Europe/Madrid',
    'krakow': 'Europe/Warsaw',
    'rotterdam': 'Europe/Amsterdam',
    'taipei': 'Asia/Taipei',
    'hong kong': 'Asia/Hong_Kong',
    'singapore': 'Asia/Singapore',
    'sydney': 'Australia/Sydney',
    'melbourne': 'Australia/Melbourne',
}

def convert_time(input_time: str, region: str) -> str:
    tz_name = None
    # Normalisation just in case
    region_lower = region.lower()
    if region_lower in ['americas', 'emea', 'pacific', 'china']:
        timezone_map = {
            'americas': 'America/Scoresbysund',
            'emea': 'Europe/Madrid',
            'pacific': 'Asia/Tokyo',
            'china': 'Asia/Shanghai'
        }
        tz_name = timezone_map[region_lower]
    else:
        # Check for city in predefined mapping
        tz_name = CITY_TIMEZONES.get(region_lower)
        if tz_name is None:
            print(f"[!] Could not find timezone for city: {region}")
            tz_name = 'Europe/Madrid'

    to_zone = tz.gettz(tz_name)
    if to_zone is None:
        to_zone = tz.gettz('Europe/Madrid')  # Ultimate fallback if timezone invalid
    standard_time = input_time.astimezone(to_zone)
    return standard_time.strftime('%H:%M:%S')
