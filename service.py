import json
import os
import time
from typing import Any, List

import requests
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_TABLE = os.environ.get("SUPABASE_TABLE")
SUPABASE_PRIMARY_KEY = os.environ.get("SUPABASE_PRIMARY_KEY", "id")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "5"))

if not all([SUPABASE_URL, SUPABASE_KEY, SUPABASE_TABLE, TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID]):
    raise RuntimeError("Missing required environment variables")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}


def fetch_new_rows(last_id: Any) -> List[dict]:
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}"
    params = {
        SUPABASE_PRIMARY_KEY: f"gt.{last_id}",
        "select": "*",
        "order": f"{SUPABASE_PRIMARY_KEY}.asc",
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()


def send_to_telegram(record: dict) -> None:
    text = json.dumps(record, ensure_ascii=False)
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": text,
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()


def fetch_max_id() -> Any:
    """Return the current maximum primary key in the table."""
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}"
    params = {
        "select": SUPABASE_PRIMARY_KEY,
        "order": f"{SUPABASE_PRIMARY_KEY}.desc",
        "limit": "1",
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    rows = response.json()
    if rows:
        return rows[0][SUPABASE_PRIMARY_KEY]
    return 0


def main() -> None:
    last_id = fetch_max_id()
    while True:
        try:
            rows = fetch_new_rows(last_id)
            if rows:
                for row in rows:
                    send_to_telegram(row)
                last_id = max(row[SUPABASE_PRIMARY_KEY] for row in rows)
        except Exception as exc:
            print(f"Error: {exc}")
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
