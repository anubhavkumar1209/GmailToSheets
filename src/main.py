import json
import os
import logging

from src.gmail_service import (
    get_gmail_service,
    fetch_unread_messages,
    get_email_details,
    mark_as_read
)
from src.sheets_service import get_sheets_service, append_row
from src.email_parser import clean_and_filter
from config import STATE_FILE


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as file:
            return set(json.load(file))
    return set()


def save_state(state):
    with open(STATE_FILE, "w") as file:
        json.dump(list(state), file)


def main():
    gmail_service = get_gmail_service()
    sheets_service = get_sheets_service(gmail_service._http.credentials)

    processed_ids = load_state()
    unread_messages = fetch_unread_messages(gmail_service)

    if not unread_messages:
        logging.info("No new unread emails found.")
        return

    processed_recent_emails = 0

    for message in unread_messages:
        msg_id = message["id"]

        if msg_id in processed_ids:
            continue

        try:
            sender, subject, date, body, labels = get_email_details(gmail_service, msg_id)
            row = clean_and_filter(sender, subject, date, body, labels)

            mark_as_read(gmail_service, msg_id)
            processed_ids.add(msg_id)

            if row:
                append_row(sheets_service, row)
                processed_recent_emails += 1
                logging.info(f"Logged email: {subject}")

        except Exception as error:
            logging.error(f"Error processing message {msg_id}: {error}")

    if processed_recent_emails == 0:
        logging.info("Completed: No unread emails received in the last 24 hours.")

    save_state(processed_ids)
    logging.info("Script execution finished.")


if __name__ == "__main__":
    main()
