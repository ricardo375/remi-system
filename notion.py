import os
from pathlib import Path
from dotenv import load_dotenv
from notion_client import Client

load_dotenv(Path('credentials/.env.notion'))

API_KEY = os.getenv('NOTION_API_KEY')
DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
client = Client(auth=API_KEY) if API_KEY else None


def add_simple_task(title: str, tags=None):
    tags = tags or []
    if not client or not DATABASE_ID:
        print('⚠️ Notion credentials missing.')
        return None
    try:
        page = client.pages.create(
            parent={'database_id': DATABASE_ID},
            properties={
                'Name': {'title': [{'text': {'content': title}}]},
                'Tags': {'multi_select': [{'name': t} for t in tags]},
            },
        )
        print('✅ Task added to Notion')
        return page
    except Exception as e:
        print(f'❌ Failed to add task: {e}')
        return None


if __name__ == '__main__':
    add_simple_task('Follow up with wedding lead', ['follow-up', 'wedding'])
