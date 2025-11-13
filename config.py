import os
from pathlib import Path

from dotenv import load_dotenv


def load_env() -> None:
    # Load .env in project root if present
    root = Path(__file__).resolve().parent
    env_path = root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        load_dotenv()  # fallback to default search


def ensure_loaded() -> None:
    # Idempotent load
    if not os.getenv("ENV_LOADED"):
        load_env()
        os.environ["ENV_LOADED"] = "1"


# Load on import so both backend and frontend can rely on env
ensure_loaded()


