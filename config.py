from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

LOG_FOLDER = BASE_DIR / "logs"
LOG_FOLDER.mkdir(exist_ok=True)