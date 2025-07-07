import shutil
from pathlib import Path

UNSORTED = Path('files/unsorted')
SORTED = Path('files/sorted')


def organize_files():
    SORTED.mkdir(parents=True, exist_ok=True)
    UNSORTED.mkdir(parents=True, exist_ok=True)
    for idx, file_path in enumerate(UNSORTED.iterdir(), start=1):
        if file_path.is_file():
            dest = SORTED / f'file_{idx}{file_path.suffix}'
            try:
                shutil.move(str(file_path), dest)
                print(f'✅ Moved {file_path.name} to {dest}')
            except Exception as e:
                print(f'❌ Failed to move {file_path}: {e}')


if __name__ == '__main__':
    organize_files()
