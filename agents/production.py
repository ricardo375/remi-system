import json
import os
from pathlib import Path
from dotenv import load_dotenv
import openai

load_dotenv(Path('credentials/.env.openai'))

API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = API_KEY
FALLBACK_PATH = Path('data/production_fallback.json')


def generate_caption(prompt: str):
    if not API_KEY:
        print('⚠️ OpenAI credentials missing. Saving prompt locally.')
        FALLBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
        json.dump({'prompt': prompt}, open(FALLBACK_PATH, 'w'), indent=2)
        return ''

    try:
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=50
        )
        caption = resp.choices[0].message.content.strip()
        print('✅ Caption generated via OpenAI')
        return caption
    except Exception as e:
        print(f'❌ Failed to generate caption: {e}')
        FALLBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
        json.dump({'prompt': prompt}, open(FALLBACK_PATH, 'w'), indent=2)
        return ''


if __name__ == '__main__':
    print(generate_caption('Write a motivational caption about teamwork'))
