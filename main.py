"""
Social Media Upload Automation
Runs daily at 10 AM IST via GitHub Actions.
For each of the 4 channels, uploads one pending video (if any)
from the corresponding Google Drive folder to YouTube + Instagram via Blotato.
"""

import os
import sys
import time

import drive_client
import blotato_client
import tracker
from config import CHANNELS, BLOTATO_API_KEY


def process_channel(channel_id: str, channel: dict):
    label = channel["label"]
    folder_id = channel["drive_folder_id"]

    print(f"\n{'='*50}")
    print(f"Processing: {label}")
    print(f"{'='*50}")

    # 1. Find the next unuploaded video
    video = drive_client.get_next_video(folder_id)
    if not video:
        print(f"  No pending videos found. Skipping.")
        tracker.log(
            channel=label,
            file_name="",
            file_id="",
            status="SKIPPED",
            notes="No videos found in Drive folder",
        )
        return

    file_id = video["id"]
    file_name = video["name"]
    print(f"  Found video: {file_name} ({file_id})")

    # Title = filename without extension
    title = os.path.splitext(file_name)[0]
    description = ""  # Add default description per channel here if needed

    public_url = None
    yt_submission = ""
    ig_submission = ""

    try:
        # 2. Temporarily make the Drive file publicly accessible
        print(f"  Making file public...")
        public_url = drive_client.make_file_public(file_id)

        # Small delay to let Drive propagate the permission
        time.sleep(3)

        # 3. Register media with Blotato
        print(f"  Uploading media to Blotato...")
        media_url = blotato_client.upload_media(public_url, BLOTATO_API_KEY)
        print(f"  Media URL: {media_url}")

        # 4. Post to YouTube
        print(f"  Posting to YouTube...")
        yt_submission = blotato_client.post_to_youtube(
            media_url=media_url,
            title=title,
            description=description,
            youtube_account_id=channel["youtube_account_id"],
            api_key=BLOTATO_API_KEY,
        )
        print(f"  YouTube submission ID: {yt_submission}")

        # 5. Post to Instagram
        print(f"  Posting to Instagram...")
        ig_submission = blotato_client.post_to_instagram(
            media_url=media_url,
            caption=title,
            instagram_account_id=channel["instagram_account_id"],
            api_key=BLOTATO_API_KEY,
        )
        print(f"  Instagram submission ID: {ig_submission}")

        # 6. Move video to 'Uploaded/' subfolder in Drive
        print(f"  Moving file to Uploaded/ folder...")
        drive_client.move_to_uploaded(file_id, folder_id)

        tracker.log(
            channel=label,
            file_name=file_name,
            file_id=file_id,
            status="SUCCESS",
            youtube_submission_id=yt_submission,
            instagram_submission_id=ig_submission,
        )
        print(f"  Done. SUCCESS")

    except Exception as e:
        error_msg = str(e)
        print(f"  ERROR: {error_msg}", file=sys.stderr)
        tracker.log(
            channel=label,
            file_name=file_name,
            file_id=file_id,
            status="FAILED",
            youtube_submission_id=yt_submission,
            instagram_submission_id=ig_submission,
            notes=error_msg[:300],
        )

    finally:
        # Always remove public access regardless of success/failure
        if public_url and file_id:
            try:
                drive_client.remove_public_access(file_id)
            except Exception:
                pass


def main():
    print("Starting Social Media Upload Automation")
    print(f"Channels to process: {len(CHANNELS)}")

    any_error = False
    for channel_id, channel in CHANNELS.items():
        try:
            process_channel(channel_id, channel)
        except Exception as e:
            print(f"Unexpected error for {channel['label']}: {e}", file=sys.stderr)
            any_error = True

    print("\nAll channels processed.")
    sys.exit(1 if any_error else 0)


if __name__ == "__main__":
    main()
