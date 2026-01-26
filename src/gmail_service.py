import os
import base64
from email import message_from_bytes
from email.header import decode_header

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from config import SCOPES


def _decode(value):
    if not value:
        return ""
    decoded_parts = decode_header(value)
    text = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            text += part.decode(encoding or "utf-8", errors="ignore")
        else:
            text += part
    return text


def get_gmail_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def fetch_unread_messages(service):
    response = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"]
    ).execute()

    return response.get("messages", [])


def get_email_details(service, msg_id):
    message = service.users().messages().get(
        userId="me",
        id=msg_id,
        format="raw"
    ).execute()

    raw_data = base64.urlsafe_b64decode(message["raw"])
    email_msg = message_from_bytes(raw_data)

    sender = _decode(email_msg.get("From"))
    subject = _decode(email_msg.get("Subject"))
    date = email_msg.get("Date", "")

    labels = ", ".join(message.get("labelIds", []))

    body = ""
    if email_msg.is_multipart():
        for part in email_msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode(errors="ignore")
                break
    else:
        body = email_msg.get_payload(decode=True).decode(errors="ignore")

    return sender, subject, date, body, labels


def mark_as_read(service, msg_id):
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()
