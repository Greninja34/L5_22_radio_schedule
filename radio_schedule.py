"""Radio station programme schedule: book, list, check and remove slots."""

import os
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE slots (id INTEGER PRIMARY KEY, show TEXT, host TEXT, "
    "start_hour INTEGER, minutes INTEGER)"
)
STUDIO_PASSWORD = os.environ.get("STUDIO_PASSWORD")


def add_slot(show, host, start_hour, minutes):
    """Book a show slot starting at start_hour and lasting minutes."""
    conn.execute(
        "INSERT INTO slots (show, host, start_hour, minutes) "
        "VALUES (?, ?, ?, ?)",
        (show, host, start_hour, minutes),
    )


def total_booked_minutes():
    """Return the total number of minutes currently booked."""
    row = conn.execute("SELECT COALESCE(SUM(minutes), 0) FROM slots")
    return row.fetchone()[0]


def slot_label(show, host):
    """Return a human-readable label for a show and its host."""
    return f"{show} hosted by {host}"


def overlap_free(start_hour, hours, next_start_hour):
    """Return True if a slot of the given length ends before the next one."""
    return start_hour + hours <= next_start_hour


def morning_shows():
    """Return the names of all shows that start before noon."""
    rows = conn.execute("SELECT show FROM slots WHERE start_hour < 12")
    return [r[0] for r in rows]


def remove_slot(slot_id):
    """Remove the slot with the given id."""
    conn.execute("DELETE FROM slots WHERE id = ?", (slot_id,))


def main():
    """Run a short demonstration of the schedule."""
    add_slot("Sunrise Beats", "Vik", 7, 60)
    add_slot("Midday Talk", "Anu", 13, 45)
    print(slot_label("Sunrise Beats", "Vik"))
    print(overlap_free(7, 1, 13), morning_shows())
    remove_slot(2)


if __name__ == "__main__":
    main()
