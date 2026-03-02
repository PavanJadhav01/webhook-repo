# 🚀 GitHub Webhook Receiver (Flask + MongoDB)

A professional, real-time GitHub Webhook processing engine built with Flask and MongoDB Atlas. This application captures events directly from GitHub, stores them with precision, and displays a live activity feed.

---

## ✨ Key Features

- **🔄 Real-time Events**: Supports `PUSH`, `PULL_REQUEST`, and `MERGE` actions.
- **📊 MongoDB Integration**: Automated storage of event data in MongoDB Atlas.
- **📅 Dynamic Timestamps**: Specialized UTC-to-String formatting for standardized audit logs.
- **🖥️ Live Dashboard**: Modern, responsive frontend that automatically polls for updates.
- **⚙️ Config-Driven**: Fully configured via environment variables for security and portability.

---

## 🛠️ Architecture & Tech Stack

- **Backend**: Python 3.x + [Flask](https://flask.palletsprojects.com/)
- **Database**: [MongoDB Atlas](https://www.mongodb.com/atlas)
- **Environment**: [python-dotenv](https://pypi.org/project/python-dotenv/)
- **Frontend**: HTML5 + Vanilla CSS + JavaScript (Auto-polling)

---

## 🚀 Quick Start Guide

### 1. Repository Setup
Clone the project and navigate to the directory:
```bash
git clone https://github.com/PavanJadhav01/webhook-repo.git
cd webhook-repo
```

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.abcde.mongodb.net/github_webhook_db
```

### 3. Installation & Execution
```powershell
# Create & Activate Virtual Environment
python -m venv venv
.\venv\Scripts\activate  # Windows

# Install Dependencies
pip install -r requirements.txt

# Start the Engine
python app.py
```
The server will be live at `http://127.0.0.1:5000`.

---

## 🔗 Connecting GitHub Webhooks

To receive live data, you must expose your local server using a tool like [ngrok](https://ngrok.com/):

1. **Expose Port**: `ngrok http 5000`
2. **Setup Webhook**: 
   - Go to your GitHub Repo -> **Settings** -> **Webhooks**.
   - **Payload URL**: `https://<your-ngrok-url>/events`
   - **Content type**: `application/json`
   - **Events**: Select **Pushes** and **Pull requests**.

---

## 📂 Project Structure

```text
webhook-repo/
├── app.py              # Core Flask application & Logic
├── requirements.txt    # Python dependencies
├── .env                # Secret environment variables
├── .gitignore          # Repository exclusions
└── templates/
    └── index.html      # Live Dashboard UI
```

---

## 📝 MongoDB Event Schema

| Field | Description |
| :--- | :--- |
| `author` | GitHub username of the actor |
| `action` | The event type (`PUSH`, `PULL_REQUEST`, `MERGE`) |
| `from_branch` | Source branch for PRs |
| `to_branch` | Target/Destination branch |
| `timestamp` | Formatted UTC string for human readability |

---

Developed for technical assessment and webhook demonstration purposes.
