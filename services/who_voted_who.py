
# :: Handle queries and formatting for discord command: who voted who

from db.db_instance import db
from db.queries import db_logic


# Get information for who voted for which teams for the day's upcomming matches
def who_voted_who() -> str | None:
    # check if an event is currently undergoing

    # if not
        # check for the most recent upcoming event
        # check if points exist
            # if not  - output negative
            # if yes
                # go to 2.1

    # if yes - (2.1)
        # grab the most recent "day" with matches still ongoing
        # print out who voted for who

    return




"""
CREATE TABLE matches(
    match_id integer PRIMARY KEY,
    team1_id integer NOT NULL,
    team2_id integer NOT NULL,
    winner_id integer,
    m_event_id integer NOT NULL,
    bracket text NOT NULL,
    kind text NOT NULL,
    date text NOT NULL,
)

CREATE TABLE votes(
    vote_id integer PRIMARY KEY,
    vote_match_id integer NOT NULL,
    vote_team_id integer NOT NULL,
    vote_player_id integer NOT NULL,
);


    desc = 
- **Swiss Stage: Round 1  ·**  {get_vct_emoji('vit')} vs {get_vct_emoji('t1')}
  - {get_vct_emoji('vit')}   `Alex`  `Ting`
  - {get_vct_emoji('t1')}   `Qiff`  `Oliver`  `Maka`
- **Swiss Stage: Round 1  ·**  {get_vct_emoji('g2')} vs {get_vct_emoji('te')}
  - {get_vct_emoji('g2')}   `Alex`  `Ting`  `Qiff`
  - {get_vct_emoji('te')}   `Oliver`  `Maka`
  
    embed.set_image(url="https://i.ytimg.com/vi/FA3f5TGNj7s/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBt2kHJKriLP0D5XXptHurNnd7a1Q")
    embed.set_footer(
        text="Fri, February 21, 2025"
    )
"""
