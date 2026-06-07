from aw_client import ActivityWatchClient
import csv

BUCKET_ID = "aw-watcher-input_DESKTOP-OTAAS9U" 

client = ActivityWatchClient("csv-export")

events = client.get_events(BUCKET_ID, limit=1000)

with open("input_activity.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # CSV headers
    writer.writerow([
        "timestamp",
        "duration",
        "presses",
        "clicks",
        "deltaX",
        "deltaY",
        "scrollX",
        "scrollY"
    ])

    for event in events:
        data = event.get("data", {})

        writer.writerow([
            event.get("timestamp"),
            event.get("duration"),
            data.get("presses", 0),
            data.get("clicks", 0),
            data.get("deltaX", 0),
            data.get("deltaY", 0),
            data.get("scrollX", 0),
            data.get("scrollY", 0)
        ])