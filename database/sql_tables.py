
# :purpose: Establish the groundwork tables for the basis of the db

import sqlite3
from database.sql_table_classes import Player, Team, Event, Match, Points


conn = sqlite3.connect('vct_pickems.db')
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")
conn.commit()


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
# players
def add_player_entry(object: Player) -> None:
    try:
        with conn:
            c.execute("INSERT INTO players (name, vlr_user, stars) VALUES (:name, :vlr_user, :stars)"
                    , object.__dict__)
    except sqlite3.IntegrityError as e:
        print(e)

def del_player_entry(player_id: int) -> None:
    with conn:
        c.execute("DELETE FROM players WHERE player_id=:player_id"
                  , {'player_id': player_id})

# teams
def add_team_entry(object: Team) -> None:
    try:
        with conn:
            c.execute("INSERT INTO teams (name, short_name) VALUES (:name, :short_name)"
                    , object.__dict__)
    except sqlite3.IntegrityError as e:
        print(e)

def del_team_entry(team_id: int) -> None:
    with conn:
        c.execute("DELETE FROM teams WHERE team_id=:team_id"
                  , {'team_id': team_id})

def get_team_id(name=None, short_name=None) -> int:
    with conn:
        c.execute("SELECT team_id FROM teams WHERE name=:name OR short_name=:short_name", {'name': name, 'short_name': short_name})
        return int(c.fetchone()[0])

# event
def add_event_entry(object: Event) -> None:
    try:
        with conn:
            c.execute("INSERT INTO events (kind, loc, intl, year, nr_teams, buyin_teams) VALUES (:kind, :loc, :intl, :year, :nr_teams, :buyin_teams)"
                    , object.__dict__)
    except sqlite3.IntegrityError as e:
        print(e)

def del_event_entry(event_id) -> None:
    with conn:
        c.execute("DELETE FROM events WHERE event_id=:event_id"
                  , {'event_id': event_id, 'loc': event_id})

# matches
def add_match_entry(object: Match) -> None:
    try:
        with conn:
            c.execute("INSERT INTO matches (team1_id, team2_id, bracket, kind, worth) VALUES (:team1_id, :team2_id, :bracket, :kind, :worth)"
                    , object.__dict__)
    except sqlite3.IntegrityError as e:
        print(e)

def del_match_entry(match_id) -> None:
    with conn:
        c.execute("DELETE FROM events WHERE match_id=:match_id"
                  , {'match_id': match_id})

# points
def add_points_entry(object: Points) -> None:
    try:
        with conn:
            c.execute("INSERT INTO points (pt_player_id, pt_event_id, nr_points, vlr_pt_id) VALUES (:pt_player_id, :pt_event_id, :nr_points, :vlr_pt_id)"
                    , object.__dict__)
    except sqlite3.IntegrityError as e:
        print(e)

def del_points_entry(points_id) -> None:
    with conn:
        c.execute("DELETE FROM points WHERE points_id=:points_id"
                  , {'points_id': points_id})


print()
print_all_tables()


"""
    CREATE TABLE players(
          player_id integer PRIMARY KEY AUTOINCREMENT,
          name text NOT NULL UNIQUE,
          vlr_user text NOT NULL UNIQUE,
          stars integer NOT NULL
        )

    CREATE TABLE teams(
          team_id integer PRIMARY KEY,
          name text NOT NULL UNIQUE,
          short_name text NOT NULL UNIQUE
        )

    CREATE TABLE events(
          event_id integer PRIMARY KEY,
          kind text NOT NULL,
          loc text NOT NULL,
          intl boolean NOT NULL,
          year integer NOT NULL,
          nr_teams integer NOT NULL,
          buyin_teams integer NOT NULL
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

    CREATE TABLE points(
          points_id integer PRIMARY KEY,
          pt_player_id integer NOT NULL,
          pt_event_id integer NOT NULL,
          nr_points dictionary NOT NULL,
          vlr_pt_id text NOT NULL,

          FOREIGN KEY (pt_player_id) REFERENCES players(player_id),
          FOREIGN KEY (pt_event_id) REFERENCES events(event_id)
    )

    ---

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

          FOREIGN KEY (player1_id) REFERENCES players(player_id),
          FOREIGN KEY (player2_id) REFERENCES players(player_id),
          FOREIGN KEY (bet_match_id) REFERENCES matches(match_id),
          FOREIGN KEY (p1_choice_id) REFERENCES teams(team_id),
          FOREIGN KEY (p1_choice_id) REFERENCES teams(team_id),
          FOREIGN KEY (winner_id) REFERENCES players(player_id)
        )
"""


conn.close()
