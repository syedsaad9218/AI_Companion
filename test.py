from aw_client import ActivityWatchClient
import json
import time
from datetime import datetime

client = ActivityWatchClient("continuous-logger")

LOG_FILE = "activitywatch_log.jsonl"

seen_events = set()

print("Logging ActivityWatch events...")

while True:
    try:
        buckets = client.get_buckets()

        with open(LOG_FILE, "a", encoding="utf-8") as f:

            for bucket_id in buckets:

                try:
                    events = client.get_events(bucket_id, limit=50)

                    for event in events:

                        event_key = (
                            bucket_id,
                            str(event.get("timestamp")),
                            str(event.get("duration"))
                        )

                        if event_key not in seen_events:
                            seen_events.add(event_key)

                            record = {
                                "logged_at": datetime.now().isoformat(),
                                "bucket": bucket_id,
                                "event": event
                            }

                            f.write(json.dumps(record, default=str) + "\n")

                except Exception as e:
                    print(f"Bucket error {bucket_id}: {e}")

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring...")

    except Exception as e:
        print("Error:", e)

    time.sleep(10)


