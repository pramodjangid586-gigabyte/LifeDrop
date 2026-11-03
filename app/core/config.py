import os
import shutil
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def resolve_database_path() -> str:
    """Resolve the SQLite database path, supporting serverless read-only environments like Vercel."""
    # 1. Custom database path from environment
    custom_path = os.getenv("DATABASE_PATH")
    if custom_path:
        return custom_path

    # 2. Serverless environment detection (Vercel / AWS Lambda)
    # The application root is read-only on Vercel; only /tmp is writable.
    if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        tmp_db = Path(tempfile.gettempdir()) / "bloodconnect.db"
        repo_db = BASE_DIR / "bloodconnect.db"
        # Seed /tmp database from repository database if available and not yet present
        if not tmp_db.exists() and repo_db.exists():
            try:
                shutil.copy2(repo_db, tmp_db)
            except Exception:
                pass
        return str(tmp_db)

    # 3. Standard local development path
    return str(BASE_DIR / "bloodconnect.db")

class Settings:
    PROJECT_NAME: str = "BloodConnect – Emergency Blood & Donor Finder"
    VERSION: str = "1.0.0"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "bloodconnect_super_secret_production_key_2026_xyz987")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    @property
    def DATABASE_PATH(self) -> str:
        return resolve_database_path()

    OUTDATED_THRESHOLD_HOURS: int = 24
    
    # Coordinates default (e.g., Delhi NCR / Central hub for realistic testing)
    DEFAULT_LAT: float = 28.6139
    DEFAULT_LNG: float = 77.2090

settings = Settings()
