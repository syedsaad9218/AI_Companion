from aw_client import ActivityWatchClient
import csv
import time
from datetime import datetime

# Replace with your actual bucket name
BUCKET_ID = "aw-watcher-input_DESKTOP-OTAAS9U"

client = ActivityWatchClient("input-csv-logger")

CSV_FILE = "input_activity.csv"

# Create CSV and header if it doesn't exist
try:
    with open(CSV_FILE, "x", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "logged_at",
            "event_timestamp",
            "duration",
            "keypresses",
            "mouse_distance"
        ])
except FileExistsError:
    pass

seen_events = set()

print("Logging input activity to CSV...")

while True:
    try:
        events = client.get_events(BUCKET_ID, limit=100)

        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            for event in events:
                event_key = (
                    str(event.get("timestamp")),
                    str(event.get("duration"))
                )

                if event_key in seen_events:
                    continue

                seen_events.add(event_key)

                data = event.get("data", {})

                writer.writerow([
                    datetime.now().isoformat(),
                    event.get("timestamp"),
                    event.get("duration"),
                    data.get("keys", 0),
                    data.get("mouse", 0)
                ])

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Logged events")

    except Exception as e:
        print("Error:", e)

    time.sleep(10)