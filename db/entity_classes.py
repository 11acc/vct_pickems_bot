
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
        return f'{self.short_name}'
    
    @property
    def fullname(self):
        return self.name

class Event():
    _tier_mapping = {
        "Champions": 1
        , "Masters": 2
    }

    def __init__(self, event_id: int, kind: str, loc: str, year: int, vlr_pickem_link: str) -> None:
        self.event_id = event_id
        self.kind = kind
        self.loc = loc
        self.year = year
        self.vlr_pickem_link = vlr_pickem_link

    def __repr__(self) -> str:
        return f'VCT {self.year} : {self.kind} {self.loc}'

    @property
    def kind_tier(self) -> int:
        return self._tier_mapping.get(self.kind, 3)

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
    def __init__(self, match_id: int, team1_id: int, team2_id: int, winner_id: int, m_event_id: int, bracket: str, kind: str, date: str, time: str) -> None:
        self.match_id = match_id
        self.team1_id = team1_id
        self.team2_id = team2_id
        self.winner_id = winner_id
        self.m_event_id = m_event_id
        self.bracket = bracket
        self.kind = kind
        self.date = date
        self.time = time

    # def __repr__(self) -> str:
    #     return f'{self.bracket}: {self.kind} · {self.team1_id} vs {self.team2_id}'


class Bet():
    def __init__(self, bet_id: int, active: bool, player1: Player, player2: Player, amount: int
                 , match: Match, p1_choice: Team, p2_choice: Team, winner=None
                 ) -> None:
        self.bet_id = bet_id
        self.active = active
        self.player1 = player1
        self.player2 = player2
        self.amount = amount
        self.match = match
        self.modifier = self.bet_modifier()
        self.p1_choice = p1_choice
        self.p2_choice = p2_choice
        self.winner = winner

    def __repr__(self) -> str:
        return f'{self.player1} vs {self.player2} · {self.amount} (x{self.modifier:.1f}) - {self.match}'

    def bet_modifier(self) -> float:
        return self.amount / self.match.worth