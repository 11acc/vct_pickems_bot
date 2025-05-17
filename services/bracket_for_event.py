
# :: Handle queries and formatting for discord command: bracket

from db.db_instance import db
from bracket.generate_config import generate_bracket_config
from bracket.generate_html import generate_bracket_html
from bracket.render_bracket import render_bracket
from utils.repo_root import get_repo_root
from utils.bracket_id import get_bracket_id


def bracket_for_event(event_id: int, year: int, region: str = None) -> str | None:
    # Generate bracket
    bracket_data = generate_bracket_config(event_id, region, year)
    bracket_html = generate_bracket_html(bracket_data)
    if not bracket_html:
        return None

    # Save in the generated imgs folder
    repo_root = get_repo_root()
    html_dir = repo_root / 'bracket' / 'generated_htmls'
    imgs_dir = repo_root / 'bracket' / 'generated_imgs'

    # Write generated html
    html_path = html_dir / f'{get_bracket_id(event_id, region, year)}.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(bracket_html)

    # Convert html to image
    render_bracket(html_path, imgs_dir, get_bracket_id(event_id, region, year))
