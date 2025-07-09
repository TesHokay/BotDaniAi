import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    token: str = os.getenv('BOT_TOKEN')
    admin_id: int = int(os.getenv('ADMIN_ID', '0'))
    db_path: str = os.getenv('DB_PATH', 'bot/db/bot.db')

settings = Settings()
