# tg-supabase-integration

This repository contains a simple Python service that forwards new rows from a Supabase table to a Telegram channel.

## Usage

1. Create a `.env` file based on the variables described below (the file must **not** be committed to the repository).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the service:
   ```bash
   python service.py
   ```

### Environment variables

| Variable | Description |
| -------- | ----------- |
| `SUPABASE_URL` | Base URL of your Supabase instance |
| `SUPABASE_KEY` | API key with access to the table |
| `SUPABASE_TABLE` | Name of the table to monitor |
| `SUPABASE_PRIMARY_KEY` | Primary key column name (default: `id`) |
| `TELEGRAM_BOT_TOKEN` | Token of the Telegram bot |
| `TELEGRAM_CHANNEL_ID` | ID of the Telegram channel to send messages to |
| `POLL_INTERVAL` | Polling interval in seconds (default: `5`) |

The service periodically checks for new rows in the configured table and sends each new record as a JSON message to the specified Telegram channel. When started, it queries the table for the current maximum primary key and will only forward rows added after that value, so existing records are not re-sent.
