# from aw_client import ActivityWatchClient
# import csv
# import time
# from datetime import datetime
# import math

# client = ActivityWatchClient("csv-logger")

# CSV_FILE = "activitywatch_log.csv"
# try:
#     with open(CSV_FILE, "x", newline="", encoding="utf-8") as f:
#         writer = csv.writer(f)
#         writer.writerow([
#             "duration",
#             "app",
#             "title",
#             "clicks",
#             "presses"

#         ])
# except FileExistsError:
#     pass

# seen_events = set()

# print("Logging ActivityWatch events to CSV...")

# while True:
#     try:
#         buckets = client.get_buckets()

#         with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
#             writer = csv.writer(f)

#             for bucket_id in buckets:

#                 try:
#                     events = client.get_events(bucket_id, limit=50)

#                     for event in events:

#                         event_key = (
#                             bucket_id,
#                             str(event.get("timestamp")),
#                             str(event.get("duration"))
#                         )

#                         if event_key in seen_events:
#                             continue

#                         seen_events.add(event_key)

#                         data = event.get("data", {})

                        # writer.writerow([
                        #     event.get("duration"),
                        #     data.get("app", ""),
                        #     data.get("title", ""),
                        #     data.get("clicks", 0),
                        #     data.get("presses", 0)
                        # ])

#                 except Exception as e:
#                     print(f"Bucket error {bucket_id}: {e}")

#         print(f"[{datetime.now().strftime('%H:%M:%S')}] Logged events")

#     except Exception as e:
#         print("Error:", e)

#     time.sleep(10)

from aw_client import ActivityWatchClient
import csv
import time
import math
from datetime import datetime

client = ActivityWatchClient("productivity-logger")

CSV_FILE = "productivity_log.csv"


try:
    with open(CSV_FILE, "x", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "app",
            "title",
            "mouse_clicks",
            "keypresses",
            "mouse_activity",
            "typing_intensity",
            "idle_time"
        ])
except FileExistsError:
    pass


def find_bucket(keyword):
    buckets = client.get_buckets()

    for bucket_id in buckets:
        if keyword.lower() in bucket_id.lower():
            return bucket_id

    return None


window_bucket = find_bucket("window")
input_bucket = find_bucket("input")
afk_bucket = find_bucket("afk")

print("Window Bucket:", window_bucket)
print("Input Bucket:", input_bucket)
print("AFK Bucket:", afk_bucket)

while True:
    try:
        app = ""
        title = ""
        mouse_clicks = 0
        keypresses = 0
        mouse_activity = 0
        typing_intensity = 0


        if window_bucket:
            events = client.get_events(window_bucket, limit=1)

            if events:
                data = events[0].get("data", {})
                app = data.get("app", "")
                title = data.get("title", "")


        if input_bucket:
            events = client.get_events(input_bucket, limit=1)

            if events:
                event = events[0]
                data = event.get("data", {})

                mouse_clicks = data.get("clicks", 0)
                keypresses = data.get("presses", 0)

                delta_x = data.get("deltaX", 0)
                delta_y = data.get("deltaY", 0)

                mouse_activity = round(
                    math.sqrt(delta_x**2 + delta_y**2),
                    2
                )

                duration = event.get("duration")

        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                app,
                title,
                mouse_clicks,
                keypresses,
                mouse_activity,
                typing_intensity,
                duration
            ])

    except Exception as e:
        print("Error:", e)

    time.sleep(3)