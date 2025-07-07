import os
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv(Path('credentials/.env.webflow'))

API_KEY = os.getenv('WEBFLOW_API_KEY')
SITE_ID = os.getenv('WEBFLOW_SITE_ID')
COLLECTION_ID = os.getenv('WEBFLOW_COLLECTION_ID')


def post_to_webflow(title: str, slug: str, body_text: str):
    if not API_KEY or not COLLECTION_ID:
        print('⚠️ Webflow credentials missing.')
        return None
    url = f'https://api.webflow.com/collections/{COLLECTION_ID}/items?live=true'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'accept-version': '1.0.0',
        'Content-Type': 'application/json',
    }
    data = {
        'name': title,
        'slug': slug,
        'body': body_text,
        'draft': False,
        'archived': False,
    }
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        resp.raise_for_status()
        print('✅ Posted to Webflow')
        print(resp.json())
        return resp.json()
    except Exception as e:
        print(f'❌ Failed to post to Webflow: {e}')
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)
        return None


if __name__ == '__main__':
    post_to_webflow('Test Post', 'test-post', 'This is a test Webflow CMS item')
