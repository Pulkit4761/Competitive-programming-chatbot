import os
from pathlib import Path
from dotenv import load_dotenv

def load_env() -> None:
    root = Path(__file__).resolve().parent
    env_path = root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        load_dotenv()  


def ensure_loaded() -> None:

    if not os.getenv("ENV_LOADED"):
        load_env()
        os.environ["ENV_LOADED"] = "1"

ensure_loaded()


