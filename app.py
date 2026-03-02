import os
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client["github_webhook_db"]
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    db = None

from datetime import datetime, timedelta

@app.route("/")
def index():
    """Main route returning simple status."""
    return render_template("index.html")

@app.route("/events", methods=["GET", "POST"])
def events():
    """Unified endpoint for GitHub Webhooks (POST) and event retrieval (GET)."""
    if request.method == "POST":
        try:
            event_type = request.headers.get("X-GitHub-Event")
            payload = request.json
            
            if not event_type or not payload:
                if not event_type:
                    return "OK", 200
                return jsonify({"error": "Invalid payload or missing event header"}), 400

            # Format UTC timestamp into readable string format (e.g., 1st March 2026 - 07:18 PM UTC)
            # Format: "1st March 2026 - 07:18 PM UTC"
            now_utc = datetime.utcnow()
            day = now_utc.day
            if 11 <= day <= 13:
                suffix = 'th'
            else:
                suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
            
            # Use platform-compatible hour formatting (Windows removes leading zero with %#I)
            ts_str = now_utc.strftime(f"{day}{suffix} %B %Y - %#I:%M %p UTC")

            event_data = {
                "timestamp": ts_str
            }

            if event_type == "push":
                event_data.update({
                    "action": "PUSH",
                    "author": payload.get("pusher", {}).get("name"),
                    "to_branch": payload.get("ref", "").split("/")[-1],
                    "from_branch": "",
                    "request_id": payload.get("head_commit", {}).get("id")
                })
            elif event_type == "pull_request":
                pr = payload.get("pull_request", {})
                action_type = "MERGE" if pr.get("merged") else "PULL_REQUEST"
                event_data.update({
                    "action": action_type,
                    "author": pr.get("user", {}).get("login"),
                    "from_branch": pr.get("head", {}).get("ref"),
                    "to_branch": pr.get("base", {}).get("ref"),
                    "request_id": pr.get("id")
                })
            else:
                return jsonify({"status": f"skipped event: {event_type}"}), 200

            if db is not None:
                db.events.insert_one(event_data)
                print(f"Stored {event_data['action']} event with STRING timestamp in MongoDB")
            else:
                print("MongoDB not connected, skipping storage")

            return jsonify({"status": "received", "action": event_data.get("action")}), 200

        except Exception as e:
            print(f"Error processing webhook: {e}")
            return jsonify({"error": str(e)}), 500

    # Handle GET request (Fetch events)
    try:
        if db is None:
            return jsonify({"error": "Database not connected"}), 500
            
        # Sort by _id descending to get latest 10 (chronological order)
        events_cursor = db.events.find({}, {"_id": 0}).sort("_id", -1).limit(10)
        
        formatted_events = []
        for event in events_cursor:
            author = event.get("author", "Unknown")
            action = event.get("action")
            from_branch = event.get("from_branch")
            to_branch = event.get("to_branch")
            
            # Retrieval Logic: Support both stored strings and legacy Date objects
            ts_val = event.get("timestamp")
            if isinstance(ts_val, datetime):
                day = ts_val.day
                if 11 <= day <= 13:
                    suffix = 'th'
                else:
                    suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
                ts_str = ts_val.strftime(f"{day}{suffix} %B %Y - %#I:%M %p UTC")
            else:
                ts_str = str(ts_val) if ts_val else "Invalid Date"

            if action == "PUSH":
                msg = f'"{author}" pushed to "{to_branch}" on {ts_str}'
            elif action == "PULL_REQUEST":
                msg = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {ts_str}'
            elif action == "MERGE":
                msg = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {ts_str}'
            else:
                msg = f"Unknown event on {ts_str}"
            
            formatted_events.append(msg)
        
        return jsonify(formatted_events), 200
    except Exception as e:
        print(f"Error fetching events: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
