
import sqlite3
from pickem_classes import Event

conn = sqlite3.connect(':memory:')  # fresh db on every run, for testing

cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE events(
               kind text,
               loc text,
               year integer,
               nr_teams integer,
               buyin_teams integer
            )""")

def insert_event(event):
    with conn:
        cursor.execute("INSERT INTO events VALUES (:kind, :loc, :year, :nr_teams, :buyin_teams)"
                , {'kind': event.kind, 'loc': event.loc, 'year': event.year
                    , 'nr_teams': event.nr_teams, 'buyin_teams': event.buyin_teams})

def get_event(event_kind):
    cursor.execute("SELECT * FROM events WHERE kind=:kind", {'kind': event_kind})
    return cursor.fetchall()

def update_event(event, new_nr_teams):
    with conn:
        cursor.execute("""UPDATE events SET nr_teams=:nr_teams
                       WHERE kind=:kind AND loc=:loc"""
                       , {'kind': event.kind, 'loc': event.loc, 'nr_teams': new_nr_teams})

def remove_event(event):
    with conn:
        cursor.execute("DELETE from events WHERE kind=:kind AND loc=:loc"
                       , {'kind': event.kind, 'loc': event.loc})


event1 = Event('Masters', 'Toronto', 2025, 12, 4)
event2 = Event('Champions', 'Paris', 2025, 16, 0)
event3 = Event('Champions', 'Glasgow', 2026, 42, 0)

insert_event(event1)
insert_event(event2)
insert_event(event3)

events = get_event('Champions')
print(events)

update_event(event3, 16) 

remove_event(event3)

cursor.execute("SELECT * FROM events")
print(cursor.fetchall())

conn.close()
