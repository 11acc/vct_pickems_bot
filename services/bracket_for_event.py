
# :: Handle queries and formatting for discord command: bracket

from bracket.generate_html import generate_bracket_html


def bracket_for_event(event_id: int) -> str | None:
    # call method to generate current bracket for given event id
    # figure out how to categorise subevent

    # data is obtained
    # call method to conver to image
    # return image path? upload url? ...?

    import sys
    sys.exit()

    bracket = generate_bracket_html(bracket_data)

    with open('bracket.html', 'w', encoding='utf-8') as f:
        f.write(bracket)
