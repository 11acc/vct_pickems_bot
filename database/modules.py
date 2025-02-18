
# :purpose: Establish the groundwork tables for the basis of the db

import os
from dotenv import load_dotenv
import sqlite3


load_dotenv()
DB_PATH = os.getenv('DB_PATH')

# /// Classes
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
            self._player = db.get_player_by_id(self.pt_player_id)
        return self._player

    @property
    def breakdown(self):
        if self._breakdown is None:
            self._breakdown = db.get_breakdown_by_self_id(self.point_id)
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

class DBInstance():
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self) -> None:
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
    
    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def execute(self, query: str, vars=()) -> None:
        try:
            self.connect()
            self.cursor.execute(query, vars)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"SQL error: {e}")
        except Exception as e:
            print(f"@reoken smth fucked happened: {e}")
    
    def fetch_one(self, query: str, vars=()) -> any:
        try:
            self.connect()
            self.cursor.execute(query, vars)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"SQL error: {e}")
            return None
    
    def fetch_all(self, query: str, vars=()) -> any:
        try:
            self.connect()
            self.cursor.execute(query, vars)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"SQL error: {e}")
            return []

    # /// Utility methods
    def print_all_tables(self) -> None:
        try:
            tables = self.fetch_all("SELECT name FROM sqlite_master WHERE type='table'")
            print(tables)
        except Exception as e:
            print(f"Error retrieving tables: {e}")

    def print_all_values(self, table: str) -> None:
        if not table.isidentifier():
            print(f"Invalid table name: {table}")
            return None
        try:
            row_vals = self.fetch_all(f"SELECT * FROM {table}")
            print(row_vals)
        except Exception as e:
            print(f"Error retrieving data from {table}: {e}")

    def add_entry(self, table: str, object) -> None:
        # Prevent invalid input table names
        if not table.isidentifier():
            print(f"Invalid input table: {table}")
            return None

        # Remove the first key -> id
        data = object.__dict__.copy()
        id_col = next(iter(data), None)
        if id_col:
            data.pop(id_col, None)
        # Remove any key that starts with "_", references to objs which aren't necessary
        data = {k: v for k, v in data.items() if not k.startswith("_")}
        if not data:
            print("No valid cols to insert")
            return None

        # SQL query and params
        params = ", ".join(data.keys())
        placeholders = ", ".join(f":{key}" for key in data.keys())
        query = f"INSERT INTO {table} ({params}) VALUES ({placeholders})"
        self.execute(query, data)

    def modify_entry(self, table: str, column: str, new_val: str, entity: str, entity_id: int) -> None:
        if not table.isidentifier() or not column.isidentifier() or not entity.isidentifier():
            print(f"Invalid input table: {table}, col: {column}, or entity: {entity}")
            return None
        query = f"UPDATE {table} SET {column}=? WHERE {entity}=?"
        self.execute(query, (new_val, entity_id))

    def del_entry(self, table: str, entity: str, entity_id: int) -> None:
        if not table.isidentifier() or not entity.isidentifier():
            print(f"Invalid input table: {table} or entity: {entity}")
            return None
        query = f"DELETE FROM {table} WHERE {entity}=?"
        self.execute(query, (entity_id,))

    def tuple_into_class(self, class_table, sql_obj: tuple) -> any:
        return class_table(*sql_obj)

    # /// Table specific util methods
    def get_player_by_id(self, player_id: int) -> Player | None:
        query = f"SELECT * FROM players WHERE player_id=?"
        sql_player = self.fetch_one(query, (player_id,))
        if not sql_player:
            print(f"Player with id {player_id} doesn't exist")
            return None
        return self.tuple_into_class(Player, sql_player)

    def point_sets_from_filters(self, **filters) -> list[Points] | None:
        # Construct filter clauses
        conditions = " AND ".join(f"{key}=?" for key in filters.keys())
        vals = tuple(filters.values())
        where_filt = f"WHERE {conditions}" if filters else ""
        # Construct query and fetch
        query = f"SELECT * FROM points {where_filt}"
        point_sets = self.fetch_all(query, vals)
        if not point_sets:
            print(f"No point sets found for filters: {filters}")
            return None
        return [self.tuple_into_class(Points, ply_pts) for ply_pts in point_sets]

    def get_breakdown_by_self_id(self, points_id: int) -> list[Player] | None:
        query = f"SELECT * FROM breakdown_pts WHERE bd_parent_points_id=?"
        bd_set = self.fetch_all(query, (points_id,))
        if not bd_set:
            print(f"No breakdown pts set found for id {points_id}")
            return None
        return [self.tuple_into_class(BreakdownPts, bd_pts) for bd_pts in bd_set]

    def breakdown_from_points_n_region(self, parent_pts_id: int, region: str) -> BreakdownPts | None:
        query = f"SELECT * FROM breakdown_pts WHERE bd_parent_points_id=? AND region=?"
        bd_set = self.fetch_one(query, (parent_pts_id, region))
        if not bd_set:
            print(f"No breakdown pts set found for parent_pts_id: {parent_pts_id} and region: {region}")
            return None
        return self.tuple_into_class(BreakdownPts, bd_set)

    def player_id_from_vlr_name(self, vlr_user: str) -> int | None:
        query = "SELECT player_id FROM players WHERE vlr_user=?"
        ply_id = self.fetch_one(query, (vlr_user,))
        if not ply_id:
            print(f"No player with vlr_user: {vlr_user}")
        return int(ply_id[0])

    def event_id_from_name(self, matched_name: str) -> int | None:
        query = "SELECT event_id FROM events WHERE loc=?"
        ev_id = self.fetch_one(query, (matched_name,))
        if not ev_id:
            print(f"No event with name: {matched_name}")
        return int(ev_id[0])

    def is_player_in_db(self, player_name: str) -> bool | None:
        query = "SELECT vlr_user FROM players WHERE vlr_user=?"
        return self.fetch_one(query, (player_name,))

    def update_total_point_sets(self) -> None:
        # Cycle all point sets and compute new total nr points from all respective breakdowns
        AllPtSets = self.point_sets_from_filters()
        for pt_set in AllPtSets:
            running_total = 0
            for a_breakdown in pt_set.breakdown:
                running_total += a_breakdown.bd_nr_points
            db.modify_entry("points", "nr_points", running_total, "points_id", pt_set.point_id)

# Create a global instance
db = DBInstance(DB_PATH)
