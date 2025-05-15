
# :: Handle queries and formatting for discord command: bracket

from datetime import datetime

from db.db_instance import db
from bracket.generate_config import generate_bracket_config
from bracket.generate_html import generate_bracket_html


def bracket_for_event(event_id: int, region: str = None, year: int = None) -> str | None:
    # Validate year
    if not year:
        year = datetime.now().year

    # Generate bracket
    bracket_data = generate_bracket_config(event_id, region)

    import json
    print(json.dumps(bracket_data, indent=4))


    # shorten team names to short names
    # expand bracket item to more width, see which image looks best
    # include icons inside each team
    # other votes go into vote-bottom



    # bracket_html = generate_bracket_html(bracket_data)

    # no region also works
    # get vote data and modify html

    # with open('bracket.html', 'w', encoding='utf-8') as f:
    #     f.write(bracket_html)

    # call method to conver to image
    # return image path? upload url? ...?
