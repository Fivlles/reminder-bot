import os
import requests
from dotenv import load_dotenv
load_dotenv()


# 1. Διαβάζουμε τα μυστικά από τις μεταβλητές περιβάλλοντος
token = os.environ["TELEGRAM_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]

# 2. Φτιάχνουμε το URL του API (όπως στη Φάση 1, χωρίς παραμέτρους)
url = f"https://api.telegram.org/bot{token}/sendMessage"

# 3. Οι παράμετροι του αιτήματος
params = {
    "chat_id": chat_id,
    "text": "Γεια από το Python script μου! 🐍",
}

# 4. Στέλνουμε το αίτημα και τυπώνουμε την απάντηση
response = requests.get(url, params=params)
print(response.json())