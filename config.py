import os
from dotenv import load_dotenv

load_dotenv()

BLOTATO_API_KEY = os.environ["BLOTATO_API_KEY"]

# Each channel maps to:
#   drive_folder_id  — the Google Drive folder where editors upload videos
#   youtube_account_id — Blotato account ID for this YouTube channel
#   instagram_account_id — Blotato account ID for this Instagram page
CHANNELS = {
    "sir_supreme": {
        "label": "Sir Supreme",
        "drive_folder_id": "11gI72zb_GVA9vqyvI1mDNbBLlqjl5pFI",  # Sir Supreme Final Edits
        "youtube_account_id": os.environ["SIR_SUPREME_YOUTUBE_ACCOUNT_ID"],
        "instagram_account_id": os.environ["SIR_SUPREME_INSTAGRAM_ACCOUNT_ID"],
    },
    "sir_supreme_kannada": {
        "label": "Sir Supreme Kannada",
        "drive_folder_id": "13GQZUTsg7-5vgUH93JeTws0cvewyuxPd",  # Sir Supreme Kannada Final Edits
        "youtube_account_id": os.environ["SIR_SUPREME_KANNADA_YOUTUBE_ACCOUNT_ID"],
        "instagram_account_id": os.environ["SIR_SUPREME_KANNADA_INSTAGRAM_ACCOUNT_ID"],
    },
    "supreme_tamilan": {
        "label": "Supreme Tamilan",
        "drive_folder_id": "1Y4siN7uikMracr3oOkygXzNlmmtU4uDx",  # Supreme Tamilan Final Edits
        "youtube_account_id": os.environ["SUPREME_TAMILAN_YOUTUBE_ACCOUNT_ID"],
        "instagram_account_id": os.environ["SUPREME_TAMILAN_INSTAGRAM_ACCOUNT_ID"],
    },
    "oxytosin": {
        "label": "Oxytosin",
        "drive_folder_id": "1IlzuqODoqDpBApdfBLSPw2V_ywwaYQCh",  # Oxytosin Final Edits
        "youtube_account_id": os.environ["OXYTOSIN_YOUTUBE_ACCOUNT_ID"],
        "instagram_account_id": os.environ["OXYTOSIN_INSTAGRAM_ACCOUNT_ID"],
    },
}
