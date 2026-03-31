import json
import os
import time

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive"]

VIDEO_MIME_TYPES = {
    "video/mp4",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-matroska",
    "video/webm",
}


def _get_service():
    raw = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    info = json.loads(raw)
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def get_next_video(folder_id: str) -> dict | None:
    """
    Returns the oldest video file in folder_id that is NOT inside an
    'Uploaded' subfolder. Returns None if no videos are pending.
    """
    service = _get_service()

    # Find or skip the 'Uploaded' subfolder ID so we can exclude it
    uploaded_folder_id = _get_uploaded_subfolder_id(service, folder_id)

    query = (
        f"'{folder_id}' in parents"
        f" and mimeType != 'application/vnd.google-apps.folder'"
        f" and trashed = false"
    )
    results = (
        service.files()
        .list(
            q=query,
            fields="files(id, name, mimeType, createdTime)",
            orderBy="createdTime",
        )
        .execute()
    )

    for f in results.get("files", []):
        if f.get("mimeType") in VIDEO_MIME_TYPES:
            return f

    return None


def make_file_public(file_id: str) -> str:
    """
    Grants anyone-with-the-link read access and returns the direct download URL.
    Uses &confirm=t to bypass Google's large-file virus scan warning page.
    """
    service = _get_service()
    service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"},
    ).execute()
    # confirm=t bypasses the virus-scan warning Google shows for large files
    return f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t"


def remove_public_access(file_id: str):
    """Removes the anyone-with-the-link permission from the file."""
    service = _get_service()
    try:
        perms = service.permissions().list(fileId=file_id, fields="permissions(id,type)").execute()
        for perm in perms.get("permissions", []):
            if perm["type"] == "anyone":
                service.permissions().delete(fileId=file_id, permissionId=perm["id"]).execute()
    except Exception:
        pass  # Non-fatal: file may have already been moved


def move_to_uploaded(file_id: str, parent_folder_id: str):
    """
    Moves the file into the 'Uploaded' subfolder inside parent_folder_id.
    Creates the subfolder if it doesn't exist.
    """
    service = _get_service()
    uploaded_id = _get_or_create_uploaded_subfolder(service, parent_folder_id)
    service.files().update(
        fileId=file_id,
        addParents=uploaded_id,
        removeParents=parent_folder_id,
        fields="id, parents",
    ).execute()


def _get_uploaded_subfolder_id(service, parent_folder_id: str) -> str | None:
    query = (
        f"'{parent_folder_id}' in parents"
        f" and mimeType = 'application/vnd.google-apps.folder'"
        f" and name = 'Uploaded'"
        f" and trashed = false"
    )
    results = service.files().list(q=query, fields="files(id)").execute()
    files = results.get("files", [])
    return files[0]["id"] if files else None


def _get_or_create_uploaded_subfolder(service, parent_folder_id: str) -> str:
    existing = _get_uploaded_subfolder_id(service, parent_folder_id)
    if existing:
        return existing
    folder = (
        service.files()
        .create(
            body={
                "name": "Uploaded",
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [parent_folder_id],
            },
            fields="id",
        )
        .execute()
    )
    return folder["id"]
