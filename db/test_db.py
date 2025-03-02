
# :: Test suite for DB queries and entity classes

import unittest
import sqlite3
import io
import contextlib

# Import the modules to test
from db_instance import DBInstance, db as global_db
from queries import Query_DB, db_logic as global_db_logic
import entity_classes

# Base class for tests which sets up an in‑memory database with the updated tables.
class TestBase(unittest.TestCase):
    def setUp(self):
        # Create a new in‑memory database for each test.
        self.db = DBInstance(":memory:")
        # Override the global DB instance in modules to point to our test DB.
        import db_instance
        db_instance.db = self.db
        global_db_logic.db = self.db
        # Create a Query_DB instance that uses our in‑memory DB.
        self.query = Query_DB()
        self.query.db = self.db

    def create_tables(self):
        # Updated table definitions.
        self.db.execute("""
            CREATE TABLE players(
                player_id integer PRIMARY KEY,
                name text NOT NULL UNIQUE,
                vlr_user text NOT NULL UNIQUE,
                stars integer NOT NULL
            )
        """)
        self.db.execute("""
            CREATE TABLE teams(
                team_id integer PRIMARY KEY,
                name text NOT NULL UNIQUE,
                short_name text NOT NULL UNIQUE
            )
        """)
        self.db.execute("""
            CREATE TABLE events(
                event_id integer PRIMARY KEY,
                kind text NOT NULL,
                loc text NOT NULL,
                year integer NOT NULL,
                vlr_pickem_link TEXT NOT NULL
            )
        """)
        self.db.execute("""
            CREATE TABLE points(
                points_id integer PRIMARY KEY,
                pt_player_id integer NOT NULL,
                pt_event_id integer NOT NULL,
                nr_points integer NOT NULL,
                FOREIGN KEY (pt_player_id) REFERENCES players(player_id),
                FOREIGN KEY (pt_event_id) REFERENCES events(event_id)
            )
        """)
        self.db.execute("""
            CREATE TABLE breakdown_pts(
                breakdown_pts_id integer PRIMARY KEY,
                bd_parent_points_id integer NOT NULL,
                bd_nr_points integer NOT NULL,
                vlr_handle text,
                region text,
                FOREIGN KEY (bd_parent_points_id) REFERENCES points(points_id)
            )
        """)
        self.db.execute("""
            CREATE TABLE stars(
                stars_id integer PRIMARY KEY,
                s_player_id integer NOT NULL,
                s_event_id integer NOT NULL UNIQUE,
                category text NOT NULL,
                FOREIGN KEY (s_player_id) REFERENCES players(player_id),
                FOREIGN KEY (s_event_id) REFERENCES events(event_id)
            )
        """)
        self.db.execute("""
            CREATE TABLE matches(
                match_id integer PRIMARY KEY,
                team1_id integer NOT NULL,
                team2_id integer NOT NULL,
                winner_id integer,
                m_event_id integer NOT NULL,
                bracket text NOT NULL,
                kind text NOT NULL,
                date text NOT NULL,
                FOREIGN KEY (team1_id) REFERENCES teams(team_id),
                FOREIGN KEY (team2_id) REFERENCES teams(team_id),
                FOREIGN KEY (m_event_id) REFERENCES events(event_id),
                CHECK (winner_id IN (team1_id, team2_id))
            )
        """)

    def tearDown(self):
        self.db.close()

# --- Tests for DBInstance ---
class TestDBInstance(TestBase):
    def test_connect_close(self):
        self.db.connect()
        self.assertIsNotNone(self.db.conn)
        self.db.close()
        self.assertIsNone(self.db.conn)

    def test_execute_fetch(self):
        self.db.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)")
        self.db.execute("INSERT INTO test (value) VALUES (?)", ("abc",))
        row = self.db.fetch_one("SELECT value FROM test WHERE id=1")
        self.assertEqual(row[0], "abc")
        rows = self.db.fetch_all("SELECT * FROM test")
        self.assertEqual(len(rows), 1)

    def test_print_all_tables(self):
        # Create a user table so that it appears in the sqlite_master list.
        self.db.execute("CREATE TABLE test_table (id INTEGER)")
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.db.print_all_tables()
        output = f.getvalue()
        self.assertIn("test_table", output)

    def test_print_all_values(self):
        self.db.execute("CREATE TABLE sample (id INTEGER PRIMARY KEY, val TEXT)")
        self.db.execute("INSERT INTO sample (val) VALUES (?)", ("hello",))
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.db.print_all_values("sample")
        output = f.getvalue()
        self.assertIn("hello", output)

    def test_add_modify_del_entry(self):
        # Create a dummy table and a dummy object.
        self.db.execute("CREATE TABLE sample (id INTEGER PRIMARY KEY, col1 TEXT, col2 TEXT)")
        class Dummy:
            def __init__(self):
                self.id = 1
                self.col1 = "a"
                self.col2 = "b"
                self._ignore = "ignore"
        dummy = Dummy()
        self.db.add_entry("sample", dummy)
        row = self.db.fetch_one("SELECT col1, col2 FROM sample")
        self.assertEqual(row, ("a", "b"))
        # Modify the entry.
        self.db.modify_entry("sample", "col1", "modified", "id", 1)
        row = self.db.fetch_one("SELECT col1 FROM sample WHERE id=1")
        self.assertEqual(row[0], "modified")
        # Delete the entry.
        self.db.del_entry("sample", "id", 1)
        row = self.db.fetch_one("SELECT * FROM sample WHERE id=1")
        self.assertIsNone(row)

    def test_is_player_in_db(self):
        # Note: Insert stars as an integer (e.g., 0).
        self.db.execute("INSERT INTO players (player_id, name, vlr_user, stars) VALUES (1, 'Alice', 'alice123', 0)")
        result = self.db.is_player_in_db("alice123")
        self.assertIsNotNone(result)

    def test_is_match_in_db(self):
        # Insert a match. Since team1_id and team2_id must be valid, we insert dummy teams and an event.
        self.db.execute("INSERT INTO teams (team_id, name, short_name) VALUES (1, 'Team A', 'A')")
        self.db.execute("INSERT INTO teams (team_id, name, short_name) VALUES (2, 'Team B', 'B')")
        self.db.execute("INSERT INTO events (event_id, kind, loc, year, vlr_pickem_link) VALUES (1, 'Kind', 'Loc', 2025, 'http://example.com')")
        self.db.execute("""
            INSERT INTO matches 
            (match_id, team1_id, team2_id, winner_id, m_event_id, bracket, kind, date)
            VALUES (1, 1, 2, 1, 1, 'Bracket', 'Kind', '2025-01-01')
        """)
        # Create a dummy match object with required attributes.
        class DummyMatch:
            team1_id = 1
            team2_id = 2
            m_event_id = 1
            bracket = "Bracket"
            kind = "Kind"
            date = "2025-01-01"
        dummy_match = DummyMatch()
        result = self.db.is_match_in_db(dummy_match)
        self.assertTrue(result)

    def test_get_player_ids_with_stars(self):
        # Insert events for foreign key integrity.
        self.db.execute("INSERT INTO events (event_id, kind, loc, year, vlr_pickem_link) VALUES (1, 'Test', 'TestLoc', 2025, 'http://test.com')")
        self.db.execute("INSERT INTO events (event_id, kind, loc, year, vlr_pickem_link) VALUES (2, 'Test', 'TestLoc', 2025, 'http://test.com')")
        # Insert stars with unique s_event_id values.
        self.db.execute("INSERT INTO stars (stars_id, s_player_id, s_event_id, category) VALUES (1, 1, 1, 'A')")
        self.db.execute("INSERT INTO stars (stars_id, s_player_id, s_event_id, category) VALUES (2, 2, 2, 'B')")
        ids = self.db.get_player_ids_with_stars()
        self.assertEqual(ids, [1, 2])

    def test_get_event_id_from_name(self):
        self.db.execute("INSERT INTO events (event_id, kind, loc, year, vlr_pickem_link) VALUES (1, 'Champions', 'NY', 2025, 'http://example.com')")
        ev_id = self.db.get_event_id_from_name("NY")
        self.assertEqual(ev_id, 1)

    def test_get_player_id_from_vlr_name(self):
        self.db.execute("INSERT INTO players (player_id, name, vlr_user, stars) VALUES (1, 'Bob', 'bob321', 0)")
        ply_id = self.db.get_player_id_from_vlr_name("bob321")
        self.assertEqual(ply_id, 1)

    def test_get_team_id_by_name(self):
        self.db.execute("INSERT INTO teams (team_id, name, short_name) VALUES (1, 'Team Bravo', 'Bravo')")
        team_id = self.db.get_team_id_by_name("Team Bravo")
        self.assertEqual(team_id, 1)

    def test_get_event_vlr_link_from_name(self):
        self.db.execute("INSERT INTO events (event_id, kind, loc, year, vlr_pickem_link) VALUES (1, 'Masters', 'LA', 2025, 'http://link.com')")
        link = self.db.get_event_vlr_link_from_name("LA")
        self.assertEqual(link, "http://link.com")

# --- Tests for Query_DB ---
class TestQueryDB(TestBase):
    def test_tuple_into_class(self):
        class Dummy:
            def __init__(self, a, b):
                self.a = a
                self.b = b
        tup = (1, 2)
        obj = self.query.tuple_into_class(Dummy, tup)
        self.assertEqual(obj.a, 1)
        self.assertEqual(obj.b, 2)

    def test_player_from_id(self):
        self.db.execute("INSERT INTO players (player_id, name, vlr_user, stars) VALUES (1, 'Alice', 'alice123', 0)")
        player = self.query.player_from_id(1)
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Alice")

    def test_event_from_id(self):
        self.db.execute("INSERT INTO events (event_id, kind, loc, year, vlr_pickem_link) VALUES (1, 'Champions', 'NY', 2025, 'http://example.com')")
        event = self.query.event_from_id(1)
        self.assertIsNotNone(event)
        self.assertEqual(event.loc, "NY")

    def test_match_from_id(self):
        self.db.execute("INSERT INTO teams (team_id, name, short_name) VALUES (1, 'Team A', 'A')")
        self.db.execute("INSERT INTO teams (team_id, name, short_name) VALUES (2, 'Team B', 'B')")
        self.db.execute("INSERT INTO events (event_id, kind, loc, year, vlr_pickem_link) VALUES (1, 'Kind', 'Loc', 2025, 'http://example.com')")
        self.db.execute("""
            INSERT INTO matches 
            (match_id, team1_id, team2_id, winner_id, m_event_id, bracket, kind, date)
            VALUES (1, 1, 2, 1, 1, 'Bracket', 'Kind', '2025-01-01')
        """)
        match = self.query.match_from_id(1)
        self.assertIsNotNone(match)
        self.assertEqual(match.bracket, "Bracket")

    def test_point_sets_from_filters(self):
        # Note: Use the correct column name "points_id"
        self.db.execute("INSERT INTO points (points_id, pt_player_id, pt_event_id, nr_points) VALUES (1, 1, 1, 10)")
        points_list = self.query.point_sets_from_filters(pt_player_id=1)
        self.assertIsNotNone(points_list)
        self.assertEqual(len(points_list), 1)
        self.assertEqual(points_list[0].nr_points, 10)

    def test_update_total_point_sets(self):
        self.db.execute("INSERT INTO points (points_id, pt_player_id, pt_event_id, nr_points) VALUES (1, 1, 1, 0)")
        # Insert two breakdown entries that sum to 15.
        self.db.execute("INSERT INTO breakdown_pts (breakdown_pts_id, bd_parent_points_id, bd_nr_points, vlr_handle, region) VALUES (1, 1, 5, 'h1', 'NA')")
        self.db.execute("INSERT INTO breakdown_pts (breakdown_pts_id, bd_parent_points_id, bd_nr_points, vlr_handle, region) VALUES (2, 1, 10, 'h2', 'EU')")
        self.query.update_total_point_sets()
        row = self.db.fetch_one("SELECT nr_points FROM points WHERE points_id=1")
        self.assertEqual(row[0], 15)

    def test_breakdowns_by_parent_point_id(self):
        self.db.execute("INSERT INTO breakdown_pts (breakdown_pts_id, bd_parent_points_id, bd_nr_points, vlr_handle, region) VALUES (1, 1, 5, 'h1', 'NA')")
        breakdowns = self.query.breakdowns_by_parent_point_id(1)
        self.assertIsNotNone(breakdowns)
        self.assertEqual(len(breakdowns), 1)
        self.assertEqual(breakdowns[0].bd_nr_points, 5)

    def test_breakdown_from_points_n_region(self):
        self.db.execute("INSERT INTO breakdown_pts (breakdown_pts_id, bd_parent_points_id, bd_nr_points, vlr_handle, region) VALUES (1, 1, 5, 'h1', 'NA')")
        bd = self.query.breakdown_from_points_n_region(1, "NA")
        self.assertIsNotNone(bd)
        self.assertEqual(bd.bd_nr_points, 5)
        # Test without a region filter.
        self.db.execute("INSERT INTO breakdown_pts (breakdown_pts_id, bd_parent_points_id, bd_nr_points, vlr_handle, region) VALUES (2, 1, 7, 'h2', 'EU')")
        bd2 = self.query.breakdown_from_points_n_region(1)
        self.assertIsNotNone(bd2)

    def test_player_star_info(self):
        # Insert an event and a star record for player_id 1.
        self.db.execute("INSERT INTO events (event_id, kind, loc, year, vlr_pickem_link) VALUES (1, 'Masters', 'LA', 2025, 'http://link.com')")
        self.db.execute("INSERT INTO stars (stars_id, s_player_id, s_event_id, category) VALUES (1, 1, 1, 'A')")
        info = self.query.player_star_info(1)
        self.assertIsNotNone(info)
        star_count, events = info
        self.assertIn("A", star_count)
        self.assertEqual(len(events), 1)

# --- Tests for entity_classes ---
class TestEntityClasses(TestBase):
    def test_player(self):
        from entity_classes import Player
        # Update: Use stars (an integer) instead of local.
        p1 = Player(1, "Alice", "alice123", 0)
        p2 = Player(1, "Alice", "alice123", 0)
        self.assertEqual(repr(p1), "0 Alice")
        self.assertEqual(p1, p2)
        self.assertEqual(hash(p1), hash(p2))

    def test_team(self):
        from entity_classes import Team
        team = Team(1, "Team Alpha", "Alpha")
        self.assertEqual(repr(team), "Alpha")
        self.assertEqual(team.fullname, "Team Alpha")

    def test_event(self):
        from entity_classes import Event
        event = Event(1, "Champions", "NY", 2025, "http://example.com")
        self.assertIn("NY", repr(event))
        self.assertEqual(event.kind_tier, 1)

    def test_points(self):
        from entity_classes import Points
        # Insert a player and a breakdown record for Points lazy properties.
        self.db.execute("INSERT INTO players (player_id, name, vlr_user, stars) VALUES (1, 'Alice', 'alice123', 0)")
        self.db.execute("INSERT INTO breakdown_pts (breakdown_pts_id, bd_parent_points_id, bd_nr_points, vlr_handle, region) VALUES (1, 1, 5, 'h1', 'NA')")
        pt = Points(1, 1, 1, 10)
        pt._player = None
        pt._breakdown = None
        # The lazy-loaded player property uses db_logic.player_from_id.
        player = pt.player
        self.assertEqual(player.name, "Alice")
        # The lazy-loaded breakdown property.
        breakdown = pt.breakdown
        self.assertEqual(len(breakdown), 1)
        self.assertEqual(breakdown[0].bd_nr_points, 5)

    def test_star(self):
        from entity_classes import Star
        # Insert a player and an event for Star lazy properties.
        self.db.execute("INSERT INTO players (player_id, name, vlr_user, stars) VALUES (1, 'Alice', 'alice123', 0)")
        self.db.execute("INSERT INTO events (event_id, kind, loc, year, vlr_pickem_link) VALUES (1, 'Masters', 'LA', 2025, 'http://link.com')")
        star = Star(1, 1, 1, "A")
        star._player = None
        star._event = None
        self.assertEqual(star.player.name, "Alice")
        self.assertEqual(star.event.loc, "LA")

    def test_bet(self):
        from entity_classes import Bet, Player, Match, Team
        # Create dummy players, a team, and a match.
        p1 = Player(1, "Alice", "alice123", 0)
        p2 = Player(2, "Bob", "bob321", 0)
        team = Team(1, "Team Alpha", "Alpha")
        match = Match(1, 1, 2, 1, 1, "Bracket", "Kind", "2025-01-01")
        # Add a 'worth' attribute to the match for bet calculations.
        match.worth = 20  
        bet = Bet(1, True, p1, p2, 40, match, team, team)
        self.assertAlmostEqual(bet.bet_modifier(), 2.0)
        self.assertIn("Alice", repr(bet))

if __name__ == '__main__':
    unittest.main()
