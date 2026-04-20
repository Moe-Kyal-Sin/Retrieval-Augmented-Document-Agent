from dotenv import load_dotenv
from pathlib import Path
import os
from openai import OpenAI

load_dotenv()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
