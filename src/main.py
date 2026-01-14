import json
import os
import logging
from datetime import datetime

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
        with open(STATE_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(list(state), f)


def main():
    gmail = get_gmail_service()
    sheets = get_sheets_service(gmail._http.credentials)

    processed = load_state()
    messages = fetch_unread_messages(gmail)

    if not messages:
        logging.info("No new unread emails.")
        return

    for msg in messages:
        msg_id = msg["id"]
        if msg_id in processed:
            continue

        try:
            sender, subject, date, body = get_email_details(gmail, msg_id)
            row = clean_and_filter(sender, subject, date, body)

            if not row:
                mark_as_read(gmail, msg_id)
                processed.add(msg_id)
                continue

            append_row(sheets, row)
            mark_as_read(gmail, msg_id)
            processed.add(msg_id)

            logging.info(f"Processed: {subject}")

        except Exception as e:
            logging.error(f"Failed email {msg_id}: {e}")

    save_state(processed)
    logging.info("Execution completed.")


if __name__ == "__main__":
    main()
