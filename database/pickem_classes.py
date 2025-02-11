
class Event():
    def __init__(self, kind: str, loc: str, year: int, nr_teams: int, buyin_teams: int) -> None:
        self.kind = kind
        self.loc = loc
        self.year = year
        self.nr_teams = nr_teams
        self.buyin_teams = buyin_teams

    def __repr__(self) -> str:
        return f'{self.kind} {self.loc} {self.year}'

class Team():
    def __init__(self, name: str, short_name: str) -> None:
        self.name = name
        self.short_name = short_name
    
    def __repr__(self) -> str:
        return f'{self.short_name}'
    
    @property
    def fullname(self):
        return self.name

class Match():
    def __init__(self, team1: Team, team2: Team, bracket: str, kind: str, worth: int) -> None:
        self.team1 = team1
        self.team2= team2
        self.bracket = bracket
        self.kind = kind
        self.worth = worth

    def __repr__(self) -> str:
        return f'{self.bracket}: {self.kind} · {self.team1} vs {self.team2}'

class Player():
    def __init__(self, name: str, vlr_usr: str, stars=None) -> None:
        self.name = name
        self.vlr_usr = vlr_usr
        self.stars = stars
    
    def __repr__(self):
        return f'{self.name}'

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


# Example event
# event = Event("Masters", "Bangkok", 2025, 8, 0)
# team1 = Team("Team Heretics", "TH")
# team2 = Team("Fun Plus Phoenix", "FPX")
# match = Match(team1, team2, "Playoffs", "Upper Semifinals", 50)
# player1 = Player("Reo", "reoken")
# player2 = Player("Qiff", "I_am_never_wrong", stars=1)
# bet = Bet(True, player1, player2, 70, match, team1, team2)

# print(bet)