
import redis
import json
import time
import sys

from database.db_utils import get_event_points, print_set_keys, print_all_keys, format_player_info


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


# -----


# total_points, per_region = get_event_points(2025, "KICKOFF")
# print("Total Points:", total_points)
# print("Per Region Breakdown:", per_region)  


# -----

print_all_keys(r)
print()

print(format_player_info(2025, "KICKOFF"))
sys.exit()

# 

"""

!vct register alex

!vct bet kickoff emea 50 qi

player 1 alex
amount: 50
player2: qi

available matches:
    - VIT vs TH : Upper Final
    - FUT vs TL : Lower Round 4

> choose option 1

what team do you want to win?

"""


def create_bet(player1, player2, amount):
    bet = {
        "player1": player1,
        "player2": player2,
        "amount": amount,
        "match": {
            "team1": team1,
            "team2": team2
        }
    }
    bet["winner"] = f"{bet['player1']}_vs_{bet['player2']}"
    return bet

bet = create_bet("I_am_never_wrong", "reoken", 50, "DRX", "GENG")
print(bet)


sys.exit()




# # Active
# bet_data = {
#     "player1": "I_am_never_wrong",
#     "player2": "reoken",
#     "amount": 50,
#     "match": {
#         "team1": "DRX",
#         "team2": "GENG"
#     }
# }
# r.zadd(
#     "bets:active:2025:KICKOFF:EMEA",
#     {json.dumps(bet_data): time.time()}  # Score = current timestamp
# )

# Past
bet_data = {
    "player1": "asap",
    "player2": "reoken",
    "amount": 30,
    "match": {
        "team1": "NRG",
        "team2": "KRU"
    },
    "winner": "player1"
}
r.zadd(
    "bets:past:2025:KICKOFF:AMERICAS",
    {json.dumps(bet_data): time.time()}  # Score = current timestamp
)
sys.exit()

print_set_keys(r, "bets")
print()

r.delete("bets:active:2025:KICKOFF:PACIFIC")

print(format_player_info(2025, "KICKOFF"))
sys.exit()



active_bets = r.zrange("bets:active:2025:KICKOFF:EMEA", 0, -1)
active_bets = [json.loads(bet) for bet in active_bets]

past_bets = r.zrange("bets:past:2025:KICKOFF:EMEA", 0, -1)
past_bets = [json.loads(bet) for bet in past_bets]


print_set_keys(r, "bets")
# print_all_keys(r)
print()
print(f"active_bets: {active_bets}")
print(f"past_bets: {past_bets}")


# r.delete("bets:active:2025:KICKOFF:EMEA")
# r.delete("bets:past:2025:KICKOFF:EMEA")








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