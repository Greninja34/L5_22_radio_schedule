import os
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE slots (id INTEGER PRIMARY KEY, show TEXT, host TEXT, "
    "start_hour INTEGER, minutes INTEGER)"
)
STUDIO_PASSWORD = os.environ.get("STUDIO_PASSWORD")
booked_minutes = 0


def addSlot(show, host, start_hour, minutes):
    global booked_minutes
    conn.execute(
        "INSERT INTO slots (show, host, start_hour, minutes) "
        "VALUES (?, ?, ?, ?)",
        (show, host, start_hour, minutes),
    )
    booked_minutes += minutes


def slotLabel(show, host):
    return "{} hosted by {}".format(show, host)


def overlapFree(start_hour, hours, next_start_hour):
    return start_hour + hours <= next_start_hour


def morningShows():
    if booked_minutes > 0:
        rows = conn.execute("SELECT show FROM slots WHERE start_hour < 12")
        return [r[0] for r in rows]
    return []


def removeSlot(slot_id):
    conn.execute("DELETE FROM slots WHERE id = ?", (slot_id,))


def main():
    addSlot("Sunrise Beats", "Vik", 7, 60)
    addSlot("Midday Talk", "Anu", 13, 45)
    print(slotLabel("Sunrise Beats", "Vik"))
    print(overlapFree(7, 1, 13), morningShows())
    removeSlot(2)


main()
