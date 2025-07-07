import os
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv(Path('credentials/.env.telegram'))

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
FALLBACK_LOG = Path('data/booking_fallback.log')


def send_booking_notification(message: str):
    if not TOKEN or not CHAT_ID:
        print('⚠️ Telegram credentials missing. Logging locally.')
        FALLBACK_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(FALLBACK_LOG, 'a') as f:
            f.write(message + '\n')
        return

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    try:
        r = requests.post(url, data={'chat_id': CHAT_ID, 'text': message}, timeout=10)
        r.raise_for_status()
        print('✅ Booking notification sent')
    except Exception as e:
        print(f'❌ Failed to send booking notification: {e}')
        FALLBACK_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(FALLBACK_LOG, 'a') as f:
            f.write(message + '\n')


if __name__ == '__main__':
    send_booking_notification('New booking received!')
