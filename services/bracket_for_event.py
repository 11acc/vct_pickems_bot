
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
    bracket_html = generate_bracket_html(bracket_data)

    # data is obtained
    # call method to conver to image
    # return image path? upload url? ...?
