import os
import json
from datetime import date
from pathlib import Path

import requests
from dotenv import load_dotenv

# --- Ρυθμίσεις ---
load_dotenv()
token = os.environ["TELEGRAM_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]
url = f"https://api.telegram.org/bot{token}/sendMessage"

# Το reminders.json βρίσκεται στον ίδιο φάκελο με το bot.py
REMINDERS_FILE = Path(__file__).parent / "reminders.json"


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
    today = date.today().day
    reminders = load_reminders()

    sent = 0
    for reminder in reminders:
        if reminder["day"] == today:
            ok = send_message(f"🔔 {reminder['message']}")
            print(("✅" if ok else "❌"), reminder["message"])
            sent += 1

    if sent == 0:
        print(f"Καμία υπενθύμιση για σήμερα ({today} του μήνα).")


if __name__ == "__main__":
    main()