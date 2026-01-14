📧 Gmail to Google Sheets Automation

Author: Anubhav Kumar
Email: anubhavrajyt@gmail.com

👋 Introduction

This project was built as part of an internship assignment to demonstrate real-world automation using Google APIs.

The goal was simple but practical:
read real unread emails from Gmail and automatically log them into a Google Sheet, without duplicating data and while following proper security practices.

This project closely mimics how small internal automation tools are built in real companies.

🎯 What This Project Does

Connects to Gmail using OAuth 2.0

Reads only unread emails from Inbox

Extracts:

Sender

Subject

Date & time

Email body (plain text)

Appends each email as a new row in Google Sheets

Marks emails as READ after processing

Ensures no duplicate emails are ever logged

🧠 Why This Project Is Useful

In many teams, people manually track important emails (invoices, job alerts, leads, etc.) in spreadsheets.
This project automates that entire process and ensures:

No manual copying

No repeated data

Safe and secure access using OAuth

🏗️ High-Level Architecture
Unread Gmail Emails
        |
        v
   Gmail API
   (OAuth 2.0)
        |
        v
  Python Automation
  - Fetch emails
  - Parse content
  - Prevent duplicates
        |
        v
 Google Sheets API
 (Append rows)

📂 Project Structure
gmail-to-sheets/
│
├── src/
│   ├── __init__.py
│   ├── gmail_service.py
│   ├── sheets_service.py
│   ├── email_parser.py
│   └── main.py
│
├── credentials/
│   └── credentials.json   (not committed)
│
├── proof/                 (screenshots & video)
│
├── config.py
├── requirements.txt
├── README.md
└── .gitignore

⚙️ How to Set Up and Run
1️⃣ Prerequisites

Python 3.x installed

A Gmail account

Google Cloud account

2️⃣ Install Dependencies
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

3️⃣ Google Cloud Setup

Create a new Google Cloud project

Enable:

Gmail API

Google Sheets API

Configure OAuth Consent Screen (External)

Create OAuth Client ID (Desktop App)

Download credentials.json and place it in:

credentials/credentials.json

4️⃣ Google Sheet Setup

Create a new Google Sheet

Rename the sheet tab to:
Gmail Logs

Add headers in first row:

From | Subject | Date | Content


Copy Spreadsheet ID and add it to config.py

5️⃣ Run the Script
python -m src.main


First run

Browser opens for Google login

Permissions are granted

Emails are logged

Emails are marked as read

Second run

No new unread emails.

🔐 OAuth Flow (Explained Simply)

Uses OAuth 2.0 Desktop Flow

User manually logs in once

Access token is saved locally (token.json)

No passwords are stored

No service accounts are used

This follows Google’s recommended security practices.

🔁 How Duplicate Emails Are Prevented

Each Gmail email has a unique message ID.

After processing an email:

Its ID is saved in processed_emails.json

The email is marked as READ

On re-running the script:

Already processed IDs are skipped

No duplicate rows are added

This makes the script safe to run multiple times.

💾 State Persistence Strategy

Method used: Local JSON file

Why this approach?

Lightweight

No database needed

Easy to explain and debug

Perfect for small automation tasks

⭐ Bonus Features Implemented

Subject-based filtering (optional)

Logging with timestamps

Large email body handling (safe truncation)

Error handling for API failures

Clean and modular code structure

⚠️ Limitations

Only plain-text email bodies are logged

Very long emails are truncated to comply with Google Sheets limits

Script is manually triggered (no scheduler included)

📸 Proof of Execution

The proof/ folder contains:

Gmail inbox screenshot (unread emails)

Google Sheet populated with data

OAuth consent screen screenshot

Short screen-recorded explanation video (2–3 minutes)