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
        "youtube_account_id": "31783",   # rahman khan (Sir Supreme)
        "instagram_account_id": "37950", # @sirsupremeofficial
    },
    "sir_supreme_kannada": {
        "label": "Sir Supreme Kannada",
        "drive_folder_id": "13GQZUTsg7-5vgUH93JeTws0cvewyuxPd",  # Sir Supreme Kannada Final Edits
        "youtube_account_id": "31785",   # sirsupremekannada
        "instagram_account_id": "37982",  # Sir Supreme Kannada Instagram
    },
    "supreme_tamilan": {
        "label": "Supreme Tamilan",
        "drive_folder_id": "1Y4siN7uikMracr3oOkygXzNlmmtU4uDx",  # Supreme Tamilan Final Edits
        "youtube_account_id": "31784",   # sirsupreme tamil
        "instagram_account_id": "37984",  # Supreme Tamilan Instagram
    },
    "oxytosin": {
        "label": "Oxytosin",
        "drive_folder_id": "1IlzuqODoqDpBApdfBLSPw2V_ywwaYQCh",  # Oxytosin Final Edits
        "youtube_account_id": "31782",   # onlyoxytosin
        "instagram_account_id": "37980",  # Oxytosin Official Instagram
    },
}
