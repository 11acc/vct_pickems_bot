
import redis
import json
import time

from database.db_utils import get_event_points, print_keys, format_player_info


r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# r.set("foo", "bar")
# print(r.get("foo"))

# Example player points for 2025 Kickoff EMEA
# event_point_key = "points:2025:KICKOFF:EMEA"

# Add player scores (ZADD)
# r.zadd(event_point_key, {
#     "reoken": 30
#     , "aniqi": 40
# })

# Get all player scores for all the regions of an event
# event_total = r.zrevrange("points:2025:KICKOFF:*", 0, -1, withscores=True)
# print(event_total)

# Get all player scores for the event
# event_rankings = r.zrevrange(event_point_key, 0, -1, withscores=True)
# print(event_rankings)

# Get player's total score for an event
# user_score = r.zscore(event_point_key, "reoken")
# print(user_score)
# Get top player for an event
# top_players = r.zrevrange(event_point_key, 0, 9, withscores=True)
# print(top_players)

print()


# r.zrem("points:2025:KICKOFF:EMEA", "aniqi")



# Active
bet_data = {
    "player1": "I_am_never_wrong",
    "player2": "reoken",
    "amount": 50,
    "match": {
        "team1": "DRX",
        "team2": "GENG"
    }
}
r.zadd(
    "bets:active:2025:KICKOFF:EMEA",
    {json.dumps(bet_data): time.time()}  # Score = current timestamp
)

# Past
bet_data = {
    "player1": "I_am_never_wrong",
    "player2": "reoken",
    "amount": 50,
    "match": {
        "team1": "DRX",
        "team2": "GENG"
    }
}
r.zadd(
    "bets:past:2025:KICKOFF:EMEA",
    {json.dumps(bet_data): time.time()}  # Score = current timestamp
)

active_bets = r.zrange("bets:active:2025:KICKOFF:EMEA", 0, -1)
past_bets = r.zrange("bets:past:2025:KICKOFF:EMEA", 0, -1)
# bets = [json.loads(bet) for bet in bets]


print_keys(r)
print()
# print(f"bets: {bets}")


r.delete("bets:active:2025:KICKOFF:EMEA")
r.delete("bets:past:2025:KICKOFF:EMEA")



# total_points, per_region = get_event_points(2025, "KICKOFF")
# print("Total Points:", total_points)
# print("Per Region Breakdown:", per_region)  

# print()


# header = f"VCT 2025 PICKEM' KICKOFF LEADERBOARD\n"
# test = "\n".join(format_player_info(2025, "KICKOFF"))

# compound_msg = header+test
# print(compound_msg)





"""
!reobot vct25 kickoff/masters/stage1-2/champs/gc

Player point storage:
    · Since players earn points for specific events, a sorted set (ZSET) will be best for
        -> fast ranking (high points first)
        -> easy retrieval of total points per event, year, or all time
    · Each point storage has the following structure
        points:<year>:<type>:<region>
        points:2025:KICKOFF:EMEA

Key Format	                    Type	            Purpose
points:<year>:<type>:<region>	Sorted Set (ZSET)	Stores player points for a specific event


"""