
# :: Classes for each db table for ease of use

class Player():
    def __init__(self, player_id: int, name: str, vlr_user: str, local: str) -> None:
        self.player_id = player_id
        self.name = name
        self.vlr_user = vlr_user
        self.local = local
    
    def __repr__(self):
        return f'{self.local} {self.name}'

    def __eq__(self, other):
        if isinstance(other, Player):
            return (self.player_id, self.name, self.vlr_user, self.local) == \
                   (other.player_id, other.name, other.vlr_user, other.local)
        return False
    
    def __hash__(self):
        return hash((self.player_id, self.name, self.vlr_user, self.local))

class Team():
    def __init__(self, team_id: int, name: str, short_name: str) -> None:
        self.team_id = team_id
        self.name = name
        self.short_name = short_name
    
    def __repr__(self) -> str:
        return f'Team({self.short_name})'
    
    @property
    def fullname(self):
        return self.name

class Event():
    _tier_mapping = {
        "Champions": 1
        , "Masters": 2
    }

    def __init__(self, event_id: int, kind: str, loc: str, year: int, ongoing: bool) -> None:
        self.event_id = event_id
        self.kind = kind
        self.loc = loc
        self.year = year
        self.ongoing = ongoing

    def __repr__(self) -> str:
        return f'VCT {self.year} : {self.kind} {self.loc}'

    @property
    def kind_tier(self) -> int:
        return self._tier_mapping.get(self.kind, 3)

class SubEvent():
    def __init__(self, subev_id: int, subev_parent_id: int, subev_match_url: str, subev_pickem_url: str, region: str) -> None:
        self.subev_id = subev_id
        self.subev_parent_id = subev_parent_id
        self.subev_match_url = subev_match_url
        self.subev_pickem_url = subev_pickem_url
        self.region = region

class Points():
    def __init__(self, point_id: int, pt_player_id: int, pt_event_id: int, nr_points: int) -> None:
        self.point_id = point_id
        self.pt_player_id = pt_player_id
        self._player = None  # Player obj class, loaded on demand
        self.pt_event_id = pt_event_id
        self.nr_points = nr_points
        self._breakdown = None  # Breakdown obj class, loaded on demand

    def __repr__(self):
        return f'Points({self.player}, {self.nr_points} points, event id: {self.pt_event_id})'
    
    @property
    def player(self):
        from .queries import db_logic  # import inside to avoid circular import
        if self._player is None:
            self._player = db_logic.player_from_id(self.pt_player_id)
        return self._player

    @property
    def breakdown(self):
        from .queries import db_logic
        if self._breakdown is None:
            self._breakdown = db_logic.breakdowns_by_parent_point_id(self.point_id)
        return self._breakdown

class BreakdownPts():
    def __init__(self, breakdown_pts_id: int, bd_parent_points_id: int, bd_nr_points: int, vlr_handle: str, region: str) -> None:
        self.breakdown_pts_id = breakdown_pts_id
        self.bd_parent_points_id = bd_parent_points_id
        self.bd_nr_points = bd_nr_points
        self.vlr_handle = vlr_handle
        self.region = region

class Star():
    def __init__(self, star_id: int, s_player_id: int, s_event_id: int, category: str) -> None:
        self.star_id = star_id
        self.s_player_id = s_player_id
        self._player = None  # Player obj class, loaded on demand
        self.s_event_id = s_event_id
        self._event = None  # Event obj class, loaded on demand
        self.category = category

    @property
    def player(self):
        from .queries import db_logic
        if self._player is None:
            self._player = db_logic.player_from_id(self.s_player_id)
        return self._player
    
    @property
    def event(self):
        from .queries import db_logic
        if self._event is None:
            self._event = db_logic.event_from_id(self.s_event_id)
        return self._event

class Match():
    def __init__(self, match_id: int, team1_id: int, team2_id: int, winner_id: int, m_event_id: int, region: str, bracket: str, kind: str, date: str, time: str, vlr_match_id: int, playoff_bracket_id: str) -> None:
        self.match_id = match_id
        self._votes = None  # Vote obj class, loaded on demand
        self.team1_id = team1_id
        self.team2_id = team2_id
        self._team1 = None  # Team obj class, loaded on demand
        self._team2 = None  # Team obj class, loaded on demand
        self.winner_id = winner_id
        self.m_event_id = m_event_id
        self.region = region
        self.bracket = bracket
        self.kind = kind
        self.date = date
        self.time = time
        self.vlr_match_id = vlr_match_id
        self.playoff_bracket_id = playoff_bracket_id

    @property
    def team1(self):
        from .queries import db_logic
        if self._team1 is None:
            self._team1 = db_logic.team_from_id(self.team1_id)
        return self._team1

    @property
    def team2(self):
        from .queries import db_logic
        if self._team2 is None:
            self._team2 = db_logic.team_from_id(self.team2_id)
        return self._team2

    @property
    def votes(self):
        from .queries import db_logic
        if self._votes is None:
            self._votes = db_logic.organised_votes_from_match_id(self.match_id)
        return self._votes

    def __repr__(self) -> str:
        return f'Match({self.bracket}: {self.kind} · {self.team1.short_name} vs {self.team2.short_name})'

class Vote():
    def __init__(self, vote_id: int, vote_match_id: int, vote_team_id: int, vote_player_id: int) -> None:
        self.vote_id = vote_id
        self.vote_match_id = vote_match_id
        self.vote_team_id = vote_team_id
        self.vote_player_id = vote_player_id
        self._player = None  # Player obj class, loaded on demand

    @property
    def player(self):
        from .queries import db_logic
        if self._player is None:
            self._player = db_logic.player_from_id(self.vote_player_id)
        return self._player

    def __repr__(self) -> str:
        return f'Vote({self.player} voted t{self.vote_team_id} in m{self.vote_match_id})'
