SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/spreadsheets"
]

SPREADSHEET_ID = "1XrCBZMmAVf3DCGtuRrMBXwI2X7U6ZJ_oX1ttGuW0DXk"
SHEET_NAME = "Gmail Logs"

STATE_FILE = "processed_emails.json"

# BONUS
SUBJECT_KEYWORD = None   # e.g. "Invoice" or None
MAX_CELL_LENGTH = 40000
