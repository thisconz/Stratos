from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    S3_ENDPOINT = os.getenv("S3_ENDPOINT")
    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
    S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
    S3_BUCKET = os.getenv("S3_BUCKET")
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()
