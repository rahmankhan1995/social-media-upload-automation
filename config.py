import os
from dotenv import load_dotenv

load_dotenv()

BLOTATO_API_KEY = os.environ["BLOTATO_API_KEY"]

# Each channel maps to:
#   drive_folder_id  — the Google Drive folder where editors upload videos
#   youtube_account_id — Blotato account ID for this YouTube channel
#   instagram_account_id — Blotato account ID for this Instagram page
# TEST MODE: Only Supreme Tamilan enabled. Re-enable others after test.
CHANNELS = {
    # "sir_supreme": {
    #     "label": "Sir Supreme",
    #     "drive_folder_id": "11gI72zb_GVA9vqyvI1mDNbBLlqjl5pFI",
    #     "youtube_account_id": "31783",
    #     "instagram_account_id": "37950",
    # },
    # "sir_supreme_kannada": {
    #     "label": "Sir Supreme Kannada",
    #     "drive_folder_id": "13GQZUTsg7-5vgUH93JeTws0cvewyuxPd",
    #     "youtube_account_id": "31785",
    #     "instagram_account_id": "37982",
    # },
    "supreme_tamilan": {
        "label": "Supreme Tamilan",
        "drive_folder_id": "1Y4siN7uikMracr3oOkygXzNlmmtU4uDx",  # Supreme Tamilan Final Edits
        "youtube_account_id": "31784",   # sirsupreme tamil
        "instagram_account_id": "37984",  # Supreme Tamilan Instagram
    },
    # "oxytosin": {
    #     "label": "Oxytosin",
    #     "drive_folder_id": "1IlzuqODoqDpBApdfBLSPw2V_ywwaYQCh",
    #     "youtube_account_id": "31782",
    #     "instagram_account_id": "37980",
    # },
}
