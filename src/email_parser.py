from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from config import MAX_CELL_LENGTH, SUBJECT_KEYWORD, EXCLUDED_SENDERS


def clean_and_filter(sender, subject, date, body, labels):
    sender_lower = sender.lower()

    for keyword in EXCLUDED_SENDERS:
        if keyword in sender_lower:
            return None

    if SUBJECT_KEYWORD and SUBJECT_KEYWORD.lower() not in subject.lower():
        return None

    try:
        email_time = parsedate_to_datetime(date)
        if email_time.tzinfo is None:
            email_time = email_time.replace(tzinfo=timezone.utc)

        if email_time < datetime.now(timezone.utc) - timedelta(hours=24):
            return None
    except Exception:
        return None

    body = body.replace("\n", " ").strip()

    if len(body) > MAX_CELL_LENGTH:
        body = body[:MAX_CELL_LENGTH] + " ...[TRUNCATED]"

    return [
        sender.strip(),
        subject.strip(),
        date.strip(),
        body,
        labels
    ]
