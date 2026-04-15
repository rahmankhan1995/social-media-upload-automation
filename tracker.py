import csv
import os
from datetime import datetime, timezone, timedelta

LOG_FILE = "upload_log.csv"
FIELDNAMES = [
    "timestamp_ist",
    "channel",
    "file_name",
    "file_id",
    "youtube_submission_id",
    "instagram_submission_id",
    "status",
    "notes",
]

IST = timezone(timedelta(hours=5, minutes=30))


def already_uploaded_today(channel_label: str) -> bool:
    """Returns True if this channel already has a SUCCESS entry today (IST)."""
    if not os.path.isfile(LOG_FILE):
        return False
    today = datetime.now(IST).strftime("%Y-%m-%d")
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (
                row.get("channel") == channel_label
                and row.get("status") == "SUCCESS"
                and row.get("timestamp_ist", "").startswith(today)
            ):
                return True
    return False


def log(
    channel: str,
    file_name: str,
    file_id: str,
    status: str,
    youtube_submission_id: str = "",
    instagram_submission_id: str = "",
    notes: str = "",
):
    now_ist = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST")
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "timestamp_ist": now_ist,
                "channel": channel,
                "file_name": file_name,
                "file_id": file_id,
                "youtube_submission_id": youtube_submission_id,
                "instagram_submission_id": instagram_submission_id,
                "status": status,
                "notes": notes,
            }
        )
