
# :purpose: Establish the groundwork tables for the basis of the db

import sqlite3

conn = sqlite3.connect('vct_pickems.db')
c = conn.cursor()

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
        self.team2 = team2
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

def print_all_tables():
    with conn:
        c.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        print(c.fetchall())


# --- Create tables:
# c.execute("PRAGMA foreign_keys = ON")
# conn.commit()

print_all_tables()

"""
    CREATE TABLE events(
          event_id integer PRIMARY KEY,
          kind text NOT NULL,
          loc text NOT NULL,
          year integer NOT NULL,
          nr_teams integer NOT NULL,
          buyin_teams integer NOT NULL
        )

    CREATE TABLE teams(
          team_id integer PRIMARY KEY,
          name text NOT NULL,
          short_name text NOT NULL
        )

    CREATE TABLE matches(
          match_id integer PRIMARY KEY,
          team1_id integer NOT NULL,
          team2_id integer NOT NULL,
          bracket text NOT NULL,
          kind text NOT NULL,
          worth integer NOT NULL,

          FOREIGN KEY (team1_id) REFERENCES teams(team_id),
          FOREIGN KEY (team2_id) REFERENCES teams(team_id)
        )

    CREATE TABLE players(
          player_id integer PRIMARY KEY,
          name text NOT NULL,
          vlr_user text NOT NULL,
          stars integer NOT NULL
        )

    CREATE TABLE bets(
          bet_id integer PRIMARY KEY,
          active boolean NOT NULL,
          player1_id integer NOT NULL,
          player2_id integer NOT NULL,
          amount integer NOT NULL,
          bet_match_id integer NOT NULL,
          p1_choice_id integer NOT NULL
          p2_choice_id integer NOT NULL
          winner_id integer NOT NULL,

          FOREIGN KEY (player1_id) REFERENCES teams(player_id),
          FOREIGN KEY (player2_id) REFERENCES teams(player_id),
          FOREIGN KEY (bet_match_id) REFERENCES teams(match_id),
          FOREIGN KEY (p1_choice_id) REFERENCES teams(team_id),
          FOREIGN KEY (p1_choice_id) REFERENCES teams(team_id),
          FOREIGN KEY (winner_id) REFERENCES teams(player_id)
        )
"""


conn.close()
