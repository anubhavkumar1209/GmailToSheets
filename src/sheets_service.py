from googleapiclient.discovery import build
from config import SPREADSHEET_ID, SHEET_NAME


def get_sheets_service(credentials):
    return build("sheets", "v4", credentials=credentials)


def append_row(service, row):
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:E",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": [row]}
    ).execute()
