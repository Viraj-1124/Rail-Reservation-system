from dotenv import load_dotenv
import os

load_dotenv()

class Settings():
    DATABASE_URL: str = os.getenv("DATABASE_URL")

setting = Settings()
# print(setting.DATABASE_URL)