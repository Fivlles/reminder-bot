import os
import json
import time
from datetime import date, datetime
from pathlib import Path

import requests
import schedule
from dotenv import load_dotenv

# --- Ρυθμίσεις ---
load_dotenv()
token = os.environ["TELEGRAM_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]
url = f"https://api.telegram.org/bot{token}/sendMessage"

# Τι ώρα θα στέλνει (από το .env, αλλιώς 09:00)
SEND_TIME = os.environ.get("SEND_TIME", "09:00")

# Το reminders.json βρίσκεται στον ίδιο φάκελο με το bot.py
REMINDERS_FILE = Path(__file__).parent / "reminders.json"


def log(text):
    """Τυπώνει μήνυμα με ημερομηνία και ώρα (για τα docker logs)."""
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {text}")


def send_message(text):
    """Στέλνει ένα μήνυμα στο Telegram και επιστρέφει True αν πέτυχε."""
    params = {"chat_id": chat_id, "text": text}
    response = requests.get(url, params=params, timeout=10)
    return response.json().get("ok", False)


def load_reminders():
    """Διαβάζει τη λίστα με τις υπενθυμίσεις από το JSON."""
    with open(REMINDERS_FILE, encoding="utf-8") as f:
        return json.load(f)


def main():
    """Στέλνει όσες υπενθυμίσεις αντιστοιχούν στη σημερινή μέρα."""
    today = date.today().day
    reminders = load_reminders()

    sent = 0
    for reminder in reminders:
        if reminder["day"] == today:
            ok = send_message(f"🔔 {reminder['message']}")
            log(("✅ " if ok else "❌ ") + reminder["message"])
            sent += 1

    if sent == 0:
        log(f"Καμία υπενθύμιση για σήμερα ({today} του μήνα).")


def run_scheduler():
    """Τρέχει συνέχεια και καλεί τη main() κάθε μέρα στις SEND_TIME."""
    log(f"Το bot ξεκίνησε. Έλεγχος κάθε μέρα στις {SEND_TIME}.")
    schedule.every().day.at(SEND_TIME).do(main)

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    run_scheduler()