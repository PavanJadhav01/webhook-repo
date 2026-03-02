# GitHub Webhook Receiver

A minimal Flask application that receives, processes, and displays GitHub webhooks in real-time.

## Features
- **Unified Endpoints**: `/events` and `/webhook` both handled.
- **Event Support**: Full support for `PUSH`, `PULL_REQUEST`, and `MERGE` events.
- **MongoDB Integration**: Stores structured event data in MongoDB Atlas.
- **Live Dashboard**: Modern UI that polls for new events every 15 seconds.
- **UTC Timestamps**: Timestamps are displayed in UTC as per technical specifications.

## Setup Instructions

### 1. Prerequisites
- Python 3.x
- MongoDB Atlas account (or local MongoDB)
- [ngrok](https://ngrok.com/) for local exposure

### 2. Installation
Clone the repository and enter the directory:
```bash
cd webhook-repo
```

Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory and add your MongoDB URI:
```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.abcde.mongodb.net/github_webhook_db?retryWrites=true&w=majority
```

### 4. Running the Server
Start the Flask application:
```bash
python app.py
```
The server will run on `http://127.0.0.1:5000`.

### 5. Exposing with ngrok
In a new terminal, run ngrok to expose your local port:
```bash
ngrok http 5000
```
Copy the `https://...` forwarding URL provided by ngrok.

### 6. GitHub Webhook Setup
1. Go to your GitHub repository -> **Settings** -> **Webhooks** -> **Add webhook**.
2. **Payload URL**: `https://<your-ngrok-url>/events`
3. **Content type**: `application/json`
4. **Events**: Select "Let me select individual events" and choose **Pushes** and **Pull requests**.
5. Click **Add webhook**.

## MongoDB Schema
Events are stored with the following structure:
- `request_id`: Commit ID or PR ID
- `author`: GitHub username
- `action`: "PUSH", "PULL_REQUEST", or "MERGE"
- `from_branch`: Source branch (if applicable)
- `to_branch`: Target branch
- `timestamp`: UTC datetime object (converted to IST for display)
