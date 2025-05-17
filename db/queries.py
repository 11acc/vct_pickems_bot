
# :: High level queries handling for table entities

from .db_instance import db
from .entity_classes import Player, Team, Event, SubEvent, Points, BreakdownPts, Star, Match, Vote


class Query_DB():
    def __init__(self):
        self.db = db

    def tuple_into_class(self, class_table, sql_obj: tuple) -> any:
        return class_table(*sql_obj)

    # /// Entity from ID
    def player_from_id(self, player_id: int) -> Player | None:
        query = f"SELECT * FROM players WHERE player_id=?"
        sql_player = self.db.fetch_one(query, (player_id,))
        if not sql_player:
            print(f"Player with id {player_id} doesn't exist")
            return None
        return self.tuple_into_class(Player, sql_player)
    
    def event_from_id(self, event_id: int) -> Event | None:
        query = f"SELECT * FROM events WHERE event_id=?"
        sql_event = self.db.fetch_one(query, (event_id,))
        if not sql_event:
            print(f"Event with id {event_id} doesn't exist")
            return None
        return self.tuple_into_class(Event, sql_event)
    
    def match_from_id(self, match_id: int) -> Match | None:
        query = "SELECT * FROM matches WHERE match_id=?"
        sql_match = self.db.fetch_one(query, (match_id,))
        if not sql_match:
            # print(f"No match with id: {match_id}")
            return None
        return self.tuple_into_class(Match, sql_match)

    def team_from_id(self, team_id: int) -> Team | None:
        query = "SELECT * FROM teams WHERE team_id=?"
        sql_team = self.db.fetch_one(query, (team_id,))
        if not sql_team:
            print(f"No team with id: {team_id}")
            return None
        return self.tuple_into_class(Team, sql_team)


    # /// Event queries
    def ongoing_event_id(self) -> int | None:
        query = "SELECT event_id FROM events WHERE ongoing=?"
        sql_event = db.fetch_one(query, (True,))
        if not sql_event:
            print(f"No currently ongoing event")
            return None
        return int(sql_event[0])


    # /// SubEvent queries
    def get_subevent_data_from_event_id(self, event_id: int, url_field: str) -> list[tuple] | None:
        query = f"SELECT region, {url_field} FROM sub_event WHERE subev_parent_id=?"
        sql_subev = self.db.fetch_all(query, (event_id,))
        if not sql_subev:
            print(f"No region or {url_field} found in sub events for event id: {event_id}")
            return None
        return sql_subev

    def subevent_region_match_urls_from_event_id(self, event_id: int) -> list[tuple] | None:
        return self.get_subevent_data_from_event_id(event_id, "subev_match_url")
        
    def subevent_region_pickem_urls_from_event_id(self, event_id: int) -> list[tuple] | None:
        return self.get_subevent_data_from_event_id(event_id, "subev_pickem_url")

    def check_event_subs(self, event_id: int) -> bool | None:
        query = "SELECT subev_id FROM sub_event WHERE subev_parent_id=?"
        sql_event = db.fetch_all(query, (event_id,))
        if not sql_event:
            print(f"No sub events for event with id: {event_id}")
            return None
        return True if len(sql_event) > 1 else False

    # /// Points queries
    def point_sets_from_filters(self, **filters) -> list[Points] | None:
        # Construct filter clauses
        conditions = " AND ".join(f"{key}=?" for key in filters.keys())
        vals = tuple(filters.values())
        where_filt = f"WHERE {conditions}" if filters else ""
        
        query = f"SELECT * FROM points {where_filt} ORDER BY nr_points DESC"
        point_sets = self.db.fetch_all(query, vals)
        if not point_sets:
            print(f"No point sets found for filters: {filters}")
            return None
        return [self.tuple_into_class(Points, ply_pts) for ply_pts in point_sets]

    def get_single_point_set(self, pt_player_id: int, pt_event_id: int) -> Points | None:
        # Get a single point set for a specific player and event.
        results = self.point_sets_from_filters(pt_player_id=pt_player_id, pt_event_id=pt_event_id)
        if results and len(results) > 0:
            return results[0]
        return None

    def update_total_point_sets(self) -> None:
        # Cycle all point sets and compute new total nr points from all respective breakdowns
        AllPtSets = self.point_sets_from_filters()
        for pt_set in AllPtSets:
            running_total = 0
            for a_breakdown in pt_set.breakdown:
                running_total += a_breakdown.bd_nr_points
            self.db.modify_entry("points", "nr_points", running_total, "points_id", pt_set.point_id)


    # /// BreakdownPts queries
    def breakdowns_by_parent_point_id(self, points_id: int) -> list[Player] | None:
        query = f"SELECT * FROM breakdown_pts WHERE bd_parent_points_id=?"
        bd_set = self.db.fetch_all(query, (points_id,))
        if not bd_set:
            print(f"No breakdown pts set found for id {points_id}")
            return None
        return [self.tuple_into_class(BreakdownPts, bd_pts) for bd_pts in bd_set]

    def breakdown_from_points_n_region(self, parent_points_id: int, region=None) -> BreakdownPts | None:
        # Check if we need to filter by region or not
        region_filter = "AND region=?"
        values = (parent_points_id, region)
        if not region:
            values = (parent_points_id,)
            region_filter = ""
        query = f"SELECT * FROM breakdown_pts WHERE bd_parent_points_id=? {region_filter}"
        bd_set = self.db.fetch_one(query, values)
        if not bd_set:
            print(f"No breakdown pts set found for values: {values}")
            return None
        return self.tuple_into_class(BreakdownPts, bd_set)


    # /// Star queries
    def player_star_info(self, player_id: int) -> tuple[dict, list] | None:
        query = "SELECT s_player_id, s_event_id, category, COUNT(*) AS star_count FROM stars WHERE s_player_id=? GROUP BY s_player_id, category ORDER BY category ASC"
        sql_stars = self.db.fetch_all(query, (player_id,))
        if not sql_stars:
            print(f"No star sets found")
            return None

        star_category_count = {}
        star_event_objs = []
        for _, event_id, category, count in sql_stars:
            star_category_count[category] = count
            star_event_objs.append(self.event_from_id(event_id))

        return star_category_count, star_event_objs


    # /// Match queries
    def match_id_from_params(self, **filters) -> int | None:
        # Construct filter clauses
        conditions = " AND ".join(f"{key}=?" for key in filters.keys())
        vals = tuple(filters.values())
        where_filt = f"WHERE {conditions}" if filters else ""
        
        query = f"SELECT match_id FROM matches {where_filt}"
        sql_match_id = self.db.fetch_one(query, vals)
        if not sql_match_id:
            # print(f"No match found for filters: {filters}")
            return None
        return int(sql_match_id[0])

    def match_id_non_winner_from_params(self, **filters) -> int | None:
        conditions = " AND ".join(f"{key}=?" for key in filters.keys())
        vals = tuple(filters.values())
        where_filt = f"WHERE {conditions} AND winner_id IS NULL"
        query = f"SELECT match_id FROM matches {where_filt}"
        sql_match_id = self.db.fetch_one(query, vals)
        if not sql_match_id:
            # print(f"No match found for filters: {filters} & winner_id being NULL")
            return None
        return int(sql_match_id[0])

    def match_objs_for_date(self, date_str: str) -> list[Match] | None:
        query = "SELECT * FROM matches WHERE date=? AND winner_id IS NULL"
        sql_matches = db.fetch_all(query, (date_str,))
        if not sql_matches:
            print(f"No matches found for date: {date_str}")
            return None
        return [self.tuple_into_class(Match, a_match) for a_match in sql_matches]

    def match_objs_from_type_filter(self, region: str, filter_val: str) -> int | None:
        # pick the right column based on playoff vs. non-playoff
        column = "bracket" if filter_val == "Playoffs" else "kind"
        query = f"SELECT * FROM matches WHERE region=? AND {column}=? AND winner_id IS NULL"
        sql_matches = self.db.fetch_all(query, (region, filter_val))
        if not sql_matches:
            # print(f"No match found for region: {region} and filter: {filter_val}")
            return None
        return [self.tuple_into_class(Match, a_match) for a_match in sql_matches]

    def match_objs_for_playoffs(self, event_id: int, region: str = None) -> int | None:
        query = "SELECT * FROM matches WHERE m_event_id=? AND bracket=?"
        params = [event_id, 'Playoffs']
        if region:
            query += " AND region=?"
            params.append(region)
        sql_matches = self.db.fetch_all(query, params)
        if not sql_matches:
            print(f"No matches found for event with id: {event_id} and maybe region: {region}")
            return None
        return [self.tuple_into_class(Match, a_match) for a_match in sql_matches]


    # /// Vote queries
    def votes_from_match_id(self, match_id: int) -> list[Vote]:
        query = "SELECT * FROM votes WHERE vote_match_id=? ORDER BY vote_player_id"
        sql_votes = db.fetch_all(query, (match_id,))
        if not sql_votes:
            print(f"No votes found for match with id: {match_id}")
        return [self.tuple_into_class(Vote, a_vote) for a_vote in sql_votes]

    def organised_votes_from_match_id(self, match_id: int) -> dict:
        query = "SELECT vote_team_id, group_concat(vote_player_id) FROM votes WHERE vote_match_id=? GROUP BY vote_team_id"
        sql_votes = db.fetch_all(query, (match_id,))
        if not sql_votes:
            print(f"No votes found for match with id: {match_id}")
        
        votes_by_team = {}
        for team_id, player_ids_str in sql_votes:
            # Split the comma-separated ply_ids and convert each to an integer
            player_ids = [int(p_id) for p_id in player_ids_str.split(',')]
            # Convert ids to objs
            team = self.team_from_id(team_id)
            players = [self.player_from_id(p_id) for p_id in player_ids]

            # If team already exists, extend the list; otherwise, create a new entry
            if team in votes_by_team:
                votes_by_team[team].extend(players)
            else:
                votes_by_team[team] = players

        return votes_by_team


# Global instance
db_logic = Query_DB()
