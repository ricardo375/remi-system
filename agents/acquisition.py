import json
import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv(Path('credentials/.env.gsheet'))

CREDENTIALS_FILE = os.getenv('GSHEET_CREDENTIALS_FILE')
SPREADSHEET_ID = os.getenv('GSHEET_SPREADSHEET_ID')

FALLBACK_PATH = Path('data/leads_fallback.json')

SCOPES = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]


def _get_sheet():
    if not CREDENTIALS_FILE or not SPREADSHEET_ID:
        return None
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE, SCOPES
        )
        client = gspread.authorize(creds)
        return client.open_by_key(SPREADSHEET_ID).sheet1
    except Exception as e:
        print(f'❌ Failed to connect to Google Sheets: {e}')
        return None


def scrape_leads(url: str):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        print('✅ Leads scraped from source')
        return resp.json()
    except Exception as e:
        print(f'❌ Failed to scrape leads: {e}')
        return []


def push_to_sheet(leads):
    sheet = _get_sheet()
    if not sheet:
        print('⚠️ Google Sheets credentials missing. Saving leads locally.')
        FALLBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
        json.dump(leads, open(FALLBACK_PATH, 'w'), indent=2)
        return

    for lead in leads:
        try:
            sheet.append_row([json.dumps(lead)])
            print('✅ Lead added to Google Sheet')
        except Exception as e:
            print(f'❌ Failed to add lead to Google Sheet: {e}')
            FALLBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
            existing = []
            if FALLBACK_PATH.exists():
                existing = json.load(open(FALLBACK_PATH))
            existing.append(lead)
            json.dump(existing, open(FALLBACK_PATH, 'w'), indent=2)


if __name__ == '__main__':
    leads = scrape_leads('https://jsonplaceholder.typicode.com/users')
    if leads:
        push_to_sheet(leads)
