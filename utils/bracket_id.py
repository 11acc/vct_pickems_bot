

def get_bracket_id(event_id: int, region: str = None, year: int = None) -> str:
    unique_id = f'{event_id}_{year}_{region.lower()}' if region else f'{event_id}_{year}'
    return f'bracket_e{unique_id}'

