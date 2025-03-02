
# :: High level queries handling for table entities

from .db_instance import db
from .entity_classes import Player, Team, Event, Points, BreakdownPts, Star, Match


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
            print(f"No match with id: {match_id}")
            return None
        return self.tuple_into_class(Match, sql_match)


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



# Global instance
db_logic = Query_DB()
