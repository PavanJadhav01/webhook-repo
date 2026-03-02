# GitHub Webhook Receiver (Flask + MongoDB)

A Flask-based backend application that receives, processes, and stores GitHub webhook events in MongoDB Atlas. The application also provides a live dashboard to display recent activity.

## ✨ Features

- Supports **push**, **pull_request**, and **merge** events
- Stores structured event data in **MongoDB Atlas**
- Displays real-time updates via **auto-refreshing dashboard**
- Uses **environment variables** for secure configuration
- Timestamps stored and displayed in **UTC**

## 🛠 Tech Stack

- **Python 3.x**
- **Flask**
- **MongoDB Atlas**
- **HTML + Vanilla JavaScript**
- **python-dotenv**

## 🚀 Setup

```bash
git clone https://github.com/PavanJadhav01/webhook-repo.git
cd webhook-repo
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Create a .env file:

```env
MONGO_URI=your_mongodb_connection_string
```

### Run the application:

```bash
python app.py
```

**Server runs at:** [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🔗 Webhook Configuration

- **Expose locally using**: `ngrok http 5000`
- **Payload URL**: `https://<ngrok-url>/webhook`
- **Content Type**: `application/json`
- **Events**: Push & Pull Request

## 📂 Project Structure

```text
webhook-repo/
├── app.py
├── requirements.txt
├── templates/
├── .env.example
└── README.md
```
