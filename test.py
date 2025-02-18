
from database.modules import db


e_list = [
      ["https://www.vlr.gg/vct-2025/?stage=241", 1]
    , ["https://www.vlr.gg/event/leaderboard/2281/champions-tour-2025-masters-bangkok/?group=08da36b9", 2]
    , ["https://www.vlr.gg/vct-2025/?stage=242", 3]
    , ["https://www.vlr.gg/vct-2025/?stage=243", 5]
]

# db.execute("ALTER TABLE events ADD vlr_pickem_link text")

for e in e_list:
    db.modify_entry("events", "vlr_pickem_link", e[0], "event_id", e[1])