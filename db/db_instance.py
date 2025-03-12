
# :: Initiate db instance and low level handling of db operations

import os
from dotenv import load_dotenv
import sqlite3


load_dotenv()
DB_PATH = os.getenv('DB_PATH')


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

    # /// Is x in DB
    def is_player_in_db(self, player_name: str) -> bool | None:
        query = "SELECT vlr_user FROM players WHERE vlr_user=?"
        return self.fetch_one(query, (player_name,))

    def is_match_in_db(self, new_match) -> bool | None:
        query = "SELECT match_id FROM matches WHERE team1_id=? AND team2_id=? AND m_event_id=? AND bracket=? AND kind=?"
        params = (
            new_match.team1_id
            , new_match.team2_id
            , new_match.m_event_id
            , new_match.bracket
            , new_match.kind
        )
        sql_match = self.fetch_one(query, params)
        if not sql_match:
            return False
        return True

    # /// Aggregate list
    def get_player_ids_with_stars(self) -> list[int] | None:
        query = "SELECT DISTINCT s_player_id FROM stars ORDER BY s_player_id ASC"
        sql_stars = self.fetch_all(query)
        if not sql_stars:
            print(f"No player_ids found in stars table")
            return None
        return [p_id for (p_id,) in sql_stars]

    # /// Specific fetch queries
    def get_event_id_from_name(self, matched_name: str) -> int | None:
        query = "SELECT event_id FROM events WHERE loc=?"
        ev_id = self.fetch_one(query, (matched_name,))
        if not ev_id:
            print(f"No event with name: {matched_name}")
            return None
        return int(ev_id[0])
    
    def get_events_in_year(self, year: int) -> list | None:
        query = "SELECT loc FROM events WHERE year=?"
        sql_events = self.fetch_all(query, (year,))
        if not sql_events:
            print(f"No events in year: {year}")
            return None
        return sql_events

    def get_player_id_from_vlr_name(self, vlr_user: str) -> int | None:
        query = "SELECT player_id FROM players WHERE vlr_user=?"
        ply_id = self.fetch_one(query, (vlr_user,))
        if not ply_id:
            print(f"No player with vlr_user: {vlr_user}")
            return None
        return int(ply_id[0])
    
    def get_team_id_by_name(self, full_name: str) -> int | None:
        query = "SELECT team_id from teams WHERE name=?"
        sql_team = self.fetch_one(query, (full_name,))
        if not sql_team:
            print(f"No team with name: {full_name}")
            return None
        return int(sql_team[0])

    def get_event_vlr_link_from_name(self, input_event: str) -> str | None:
        query = "SELECT vlr_pickem_link FROM events WHERE loc=?"
        return self.fetch_one(query, (input_event,))[0]

    def get_match_without_winner(self, new_match) -> int | None:
        query = "SELECT match_id FROM matches WHERE team1_id=? AND team2_id=? AND winner_id IS NULL AND m_event_id=? AND bracket=? AND kind=?"
        params = (
            new_match.team1_id
            , new_match.team2_id
            , new_match.m_event_id
            , new_match.bracket
            , new_match.kind
        )
        sql_match = self.fetch_one(query, params)
        return int(sql_match[0]) if sql_match else None

    def get_next_upcoming_match_date(self, input_date: str) -> list | None:
        query = "SELECT DISTINCT date FROM matches WHERE date(date) > date(?) ORDER BY date(date) LIMIT 1"
        sql_date = db.fetch_one(query, (input_date,))
        if not sql_date:
            print(f"No further matches after date: {input_date}")
            return None
        return sql_date[0]

    # /// Update specific row properties
    def update_match_winner(self, match_id: int, winner_id: int) -> None:
        self.modify_entry("matches", "winner_id", winner_id, "match_id", match_id)



# Global instance
db = DBInstance(DB_PATH)
