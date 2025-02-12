
class Player():
    def __init__(self, name: str, vlr_user: str, stars=None) -> None:
        self.name = name
        self.vlr_user = vlr_user
        self.stars = stars
    
    def __repr__(self):
        return f'{self.name}'

class Team():
    def __init__(self, name: str, short_name: str) -> None:
        self.name = name
        self.short_name = short_name
    
    def __repr__(self) -> str:
        return f'{self.short_name}'
    
    @property
    def fullname(self):
        return self.name

class Event():
    def __init__(self, kind: str, loc: str, intl: bool, year: int, nr_teams: int, buyin_teams: int) -> None:
        self.kind = kind
        self.loc = loc
        self.intl = intl
        self.year = year
        self.nr_teams = nr_teams
        self.buyin_teams = buyin_teams

    def __repr__(self) -> str:
        return f'{self.kind} {self.loc} {self.year}'

class Match():
    def __init__(self, team1_id: int, team2_id: int, bracket: str, kind: str, worth: int) -> None:
        self.team1_id = team1_id
        self.team2_id = team2_id
        self.bracket = bracket
        self.kind = kind
        self.worth = worth

    # def __repr__(self) -> str:
    #     return f'{self.bracket}: {self.kind} · {self.team1} vs {self.team2}'

class Points():
    def __init__(self, pt_player_id: int, pt_event_id: int, nr_points: int, vlr_pt_id: str) -> None:
        self.pt_player_id = pt_player_id
        self.pt_event_id = pt_event_id
        self.nr_points = nr_points
        self.vlr_pt_id = vlr_pt_id

    # def __repr__(self):
    #     return f'{self.player} has {self.nr_points} points for event: {self.event}'

class Bet():
    def __init__(self, active: bool, player1: Player, player2: Player, amount: int
                 , match: Match, p1_choice: Team, p2_choice: Team, winner=None
                 ) -> None:
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
