from config import MAX_CELL_LENGTH, SUBJECT_KEYWORD


def clean_and_filter(sender, subject, date, body):
    if SUBJECT_KEYWORD and SUBJECT_KEYWORD.lower() not in subject.lower():
        return None

    body = body.replace("\n", " ").strip()

    if len(body) > MAX_CELL_LENGTH:
        body = body[:MAX_CELL_LENGTH] + " ...[TRUNCATED]"

    return [sender.strip(), subject.strip(), date.strip(), body]
