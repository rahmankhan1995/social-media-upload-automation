import time
import requests

BASE_URL = "https://backend.blotato.com/v2"


def _headers(api_key: str) -> dict:
    return {"blotato-api-key": api_key, "Content-Type": "application/json"}


def upload_media(public_url: str, api_key: str) -> str:
    """
    Registers a publicly accessible video URL with Blotato.
    Returns the Blotato media URL to use when publishing.
    """
    resp = requests.post(
        f"{BASE_URL}/media",
        json={"url": public_url},
        headers=_headers(api_key),
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    # Blotato returns the processed media URL
    return data.get("url") or data.get("mediaUrl") or public_url


def post_to_youtube(
    media_url: str,
    title: str,
    description: str,
    youtube_account_id: str,
    api_key: str,
) -> str:
    """Publishes a video to YouTube via Blotato. Returns the postSubmissionId."""
    payload = {
        "post": {
            "accountId": int(youtube_account_id),
            "content": {
                "platform": "youtube",
                "text": description or title,
                "mediaUrls": [media_url],
                "title": title,
                "isMadeForKids": False,
            },
        }
    }
    resp = requests.post(
        f"{BASE_URL}/posts",
        json=payload,
        headers=_headers(api_key),
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json().get("postSubmissionId", "")


def post_to_instagram(
    media_url: str,
    caption: str,
    instagram_account_id: str,
    api_key: str,
) -> str:
    """Publishes a video Reel to Instagram via Blotato. Returns the postSubmissionId."""
    payload = {
        "post": {
            "accountId": int(instagram_account_id),
            "content": {
                "platform": "instagram",
                "text": caption,
                "mediaUrls": [media_url],
                "format": "reel",
            },
        }
    }
    resp = requests.post(
        f"{BASE_URL}/posts",
        json=payload,
        headers=_headers(api_key),
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json().get("postSubmissionId", "")
