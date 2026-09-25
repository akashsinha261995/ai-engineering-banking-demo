import os

from dotenv import load_dotenv


load_dotenv()


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")


if not OPENROUTER_API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY is not configured"
    )

if not OPENROUTER_MODEL:
    raise RuntimeError(
        "OPENROUTER_MODEL is not configured"
    )

if not OPENROUTER_BASE_URL:
    raise RuntimeError(
        "OPENROUTER_BASE_URL is not configured"
    )