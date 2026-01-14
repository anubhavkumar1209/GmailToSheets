# 📄 README.md — Gmail to Google Sheets Automation

---

## 1️⃣ High-Level Architecture Diagram

The architecture diagram represents the complete flow of how unread Gmail emails are processed and stored in Google Sheets.

### Flow Explanation (in simple words):

- The system starts by reading unread emails from Gmail  
- Emails are accessed securely using Gmail API with OAuth 2.0  
- A Python automation script processes each email  
- Email content is parsed to extract useful information  
- A duplicate check ensures the same email is not processed again  
- New emails are added to Google Sheets  
- Successfully processed emails are marked as READ

- <img width="1536" height="1024" alt="ChatGPT Image Jan 14, 2026, 05_38_17 PM" src="https://github.com/user-attachments/assets/a74cfb10-de02-4243-9ba9-60949d044ad2" />


👉 The diagram visually shows how data flows from **Gmail → Python → Google Sheets**.

---

## 2️⃣ Step-by-Step Setup Instructions

### Step 1: Prerequisites

Before starting, make sure you have:

- Python 3 installed on your system  
- A Google account  
- Access to Google Cloud Console  

---

### Step 2: Clone the Project & Install Dependencies

```bash
git clone <your-repository-link>
cd gmail-to-sheets
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### Step 3: Google Cloud Configuration

- Open **Google Cloud Console**
- Create a new project
- Enable the following APIs:
  - **Gmail API**
  - **Google Sheets API**
- Configure **OAuth Consent Screen**
- Create **OAuth 2.0 Client ID (Desktop Application)**
- Download `credentials.json`
- Place it inside the `credentials/` folder of the project

---

### Step 4: Google Sheet Setup

- Create a new Google Sheet
- Add the following headers in the first row:

```
From | Subject | Date | Content
```

- Copy the **Spreadsheet ID** from the Google Sheet URL
- Paste the Spreadsheet ID into the project configuration file

---

### Step 5: Run the Script (Local)

```bash
python -m src.main
```

---

## 🐳 6️⃣ Docker Setup (Optional)

Docker allows you to run this project in an isolated and consistent environment without setting up Python locally.

### Step 1: Prerequisites

- Docker installed on your system  
- Docker Desktop running  

---

### Step 2: Dockerfile (Project Root)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "src.main"]
```

---

### Step 3: Build Docker Image

```bash
docker build -t gmail-to-sheets .
```

---

### Step 4: Run Docker Container

```bash
docker run -it \
  -v $(pwd)/credentials:/app/credentials \
  -v $(pwd)/token.json:/app/token.json \
  -v $(pwd)/processed_emails.json:/app/processed_emails.json \
  gmail-to-sheets
```

> The volume mounts ensure OAuth tokens and state files persist outside the container.

---

## 3️⃣ Technical Explanation

### 🔐 OAuth Flow Used

The project uses **OAuth 2.0 Desktop Flow**.

- On the first run, a browser opens for Google login  
- User grants permission to Gmail and Google Sheets  
- A `token.json` file is created  
- On future runs, the token is reused automatically  
- No need to log in again every time  

This ensures secure and authorized access to user data.

---

### 🔁 Duplicate Prevention Logic

Duplicate entries are avoided using a two-step approach:

#### Unread Emails Only
- Only emails with the `UNREAD` label are fetched  

#### Message ID Check
- Each Gmail email has a unique Message ID  
- The script checks if this ID already exists  
- If yes → email is skipped  
- If no → email is processed and stored  

This guarantees **no duplicate rows in Google Sheets**.

---

### 💾 State Persistence Method

To remember already processed emails, the project uses local state storage.

- A file named `processed_emails.json` is used  
- It stores Message IDs of processed emails  
- Even if the script stops or restarts, data is not lost  
- No database is required  

This method is simple, lightweight, and effective.

---

## 4️⃣ Challenge Faced & Solution

### Challenge
Handling large and multipart emails.

### Problem
- Some emails contain both HTML and plain text  
- Large content caused Google Sheets API errors due to cell size limits  

### Solution
- Implemented recursive parsing to extract only `text/plain`  
- Ignored HTML formatting  
- Limited email content to **4,000 characters**  
- Ensured smooth insertion into Google Sheets  

This made the system stable and API-friendly.

---

## 5️⃣ Limitations of the Solution

- Only plain text emails are supported  
- HTML formatting is ignored  
- Attachments are not downloaded  
- Script must be run manually or via cron job  
- High email volume may hit Google API rate limits  

---
