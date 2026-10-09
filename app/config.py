"""Local configuration. Never store API keys in the repository."""
from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

MODEL_ID = os.getenv("GEMINI_MODEL", "gemini-3.6-flash").strip()
FALLBACK_MODEL_ID = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.5-flash-lite").strip()
ENABLE_LIVE_RESEARCH = os.getenv("ENABLE_LIVE_RESEARCH", "false").strip().lower() in {"true", "1", "yes", "on"}
DATA_PATH = ROOT / "data" / "market_snapshot.json"
