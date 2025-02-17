
# :purpose: Establish the groundwork tables for the basis of the db

import os
from dotenv import load_dotenv
import sqlite3


load_dotenv()
DB_PATH = os.getenv('DB_PATH')

# /// Classes
class DBInstance():
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
    
    def execute(self, query, vars=()):
        self.connect()
        self.cursor.execute(query, vars)
        self.conn.commit()
    
    def fetch_one(self, query, vars=()):
        self.connect()
        self.cursor.execute(query, vars)
        return self.cursor.fetchone()
    
    def fetch_all(self, query, vars=()):
        self.connect()
        self.cursor.execute(query, vars)
        return self.cursor.fetchall()
    
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

class Player():
    def __init__(self, player_id: int, name: str, vlr_user: str, stars: int, local: str) -> None:
        self.player_id = player_id
        self.name = name
        self.vlr_user = vlr_user
        self.stars = stars
        self.local = local
    
    def __repr__(self):
        return f'{self.local} {self.name}'

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
    def __init__(self, event_id: int, kind: str, loc: str, year: int) -> None:
        self.event_id = event_id
        self.kind = kind
        self.loc = loc
        self.year = year

    def __repr__(self) -> str:
        return f'{self.kind} {self.loc} {self.year}'

class Match():
    def __init__(self, match_id: int, team1_id: int, team2_id: int, bracket: str, kind: str, worth: int) -> None:
        self.match_id = match_id
        self.team1_id = team1_id
        self.team2_id = team2_id
        self.bracket = bracket
        self.kind = kind
        self.worth = worth

    # def __repr__(self) -> str:
    #     return f'{self.bracket}: {self.kind} · {self.team1} vs {self.team2}'

class Points():
    def __init__(self, point_id: int, pt_player_id: int, pt_event_id: int, nr_points: int) -> None:
        self.point_id = point_id
        self.pt_player_id = pt_player_id
        self._player = None  # Player obj class, loaded on demand
        self.pt_event_id = pt_event_id
        self.nr_points = nr_points
        self._breakdown = None  # Breakdown obj class, loaded on demand

    def __repr__(self):
        return f'[{self.player}, {self.nr_points} points, event id: {self.pt_event_id}]'
    
    @property
    def player(self):
        if self._player is None:
            self._player = get_player_by_id(self.pt_player_id)
        return self._player

    @property
    def breakdown(self):
        if self._breakdown is None:
            self._breakdown = get_breakdown_by_self_id(self.point_id)
        return self._breakdown

class BreakdownPts():
    def __init__(self, breakdown_pts_id: int, bd_parent_points_id: int, bd_nr_points: int, vlr_handle: str, region: str) -> None:
        self.breakdown_pts_id = breakdown_pts_id
        self.bd_parent_points_id = bd_parent_points_id
        self.bd_nr_points = bd_nr_points
        self.vlr_handle = vlr_handle
        self.region = region

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


# /// SQL util methods
def print_all_tables() -> None:
    with conn:
        c.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        print(c.fetchall())

def print_all_values(table: str) -> None:
    with conn:
        c.execute(f"SELECT * FROM {table}")
        print(c.fetchall())


# /// Table util methods
# global
def tuple_into_class(class_table, sql_obj: tuple) -> any:
    return class_table(*sql_obj)

def fetch_one_from_db(query: str, variables: tuple) -> any:
    with conn:
        c.execute(query, variables)
        return c.fetchone()

def fetch_all_from_db(query: str, variables: tuple) -> list:
    with conn:
        c.execute(query, variables)
        return c.fetchall()

def modify_entry(table: str, entity: str, entity_id: int, column, new_val) -> None:
    with conn:
        c.execute(f"UPDATE {table} SET {column}='{new_val}' WHERE {entity}=?", (entity_id,))

def del_entry(table: str, entity: str, entity_id: int) -> None:
    with conn:
        c.execute(f"DELETE FROM {table} WHERE {entity}=?", (entity_id,))

# players
def add_player_entry(object: Player) -> None:
    try:
        with conn:
            c.execute("INSERT INTO players (name, vlr_user, stars) VALUES (:name, :vlr_user, :stars)"
                    , object.__dict__)
    except sqlite3.IntegrityError as e:
        print(e)

def get_player_by_id(player_id: int) -> Player:
    with conn:
        c.execute("SELECT * FROM players WHERE player_id=:player_id"
                  , {'player_id': player_id})
        sql_player = c.fetchone()
    if not sql_player:
        print(f"Player with id {player_id} doesn't exist")
        return None
    return tuple_into_class(Player, sql_player)

# teams
def add_team_entry(object: Team) -> None:
    try:
        with conn:
            c.execute("INSERT INTO teams (name, short_name) VALUES (:name, :short_name)"
                    , object.__dict__)
    except sqlite3.IntegrityError as e:
        print(e)

def get_team_id(name=None, short_name=None) -> int:
    with conn:
        c.execute("SELECT team_id FROM teams WHERE name=:name OR short_name=:short_name", {'name': name, 'short_name': short_name})
        return int(c.fetchone()[0])

# event
def add_event_entry(object: Event) -> None:
    try:
        with conn:
            c.execute("INSERT INTO events (kind, loc, year) VALUES (:kind, :loc, :year)"
                    , object.__dict__)
    except sqlite3.IntegrityError as e:
        print(e)

# matches
def add_match_entry(object: Match) -> None:
    try:
        with conn:
            c.execute("INSERT INTO matches (team1_id, team2_id, bracket, kind, worth) VALUES (:team1_id, :team2_id, :bracket, :kind, :worth)"
                    , object.__dict__)
    except sqlite3.IntegrityError as e:
        print(e)

# points
def add_points_entry(object: Points) -> None:
    try:
        with conn:
            c.execute("INSERT INTO points (pt_player_id, pt_event_id, nr_points) VALUES (:pt_player_id, :pt_event_id, :nr_points)"
                    , object.__dict__)
    except sqlite3.IntegrityError as e:
        print(e)

def get_breakdown_by_self_id(points_id: int) -> any:
    with conn:
        c.execute("SELECT * FROM breakdown_pts WHERE bd_parent_points_id=:bd_parent_points_id"
                  , {'bd_parent_points_id': points_id})
        bd_set = c.fetchall()
    if not bd_set:
        print(f"No points set found for id {points_id}")
        return None
    return [tuple_into_class(BreakdownPts, bd_pts) for bd_pts in bd_set]

# breakdown
def add_breakdown_entry(object: BreakdownPts) -> None:
    try:
        with conn:
            c.execute("INSERT INTO breakdown_pts (bd_parent_points_id, bd_nr_points, vlr_handle, region) VALUES (:bd_parent_points_id, :bd_nr_points, :vlr_handle, :region)"
                    , object.__dict__)
    except sqlite3.IntegrityError as e:
        print(e)


# -----------------------------------------------------------------------------------------------------------


# Create a global instance
db = DBInstance()

