import os
from dataclasses import dataclass

@dataclass
class Settings:
    token: str = os.getenv('BOT_TOKEN', '7783237838:AAFn3X9MqTt-SvJiSA-6KdxJ82ppYyJgoao')
    admin_id: int = int(os.getenv('ADMIN_ID', '895330910'))
    db_path: str = os.getenv('DB_PATH', 'bot/db/bot.db')

settings = Settings()
