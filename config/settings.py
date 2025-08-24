import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to KB JSON file
KB_FILE_PATH = os.path.join(BASE_DIR, "data", "kb.json")

# Read from .env, fallback to "logs" if not set
LOG_DIR = os.getenv("LOG_DIR", "logs")