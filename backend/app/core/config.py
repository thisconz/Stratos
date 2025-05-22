from dotenv import load_dotenv
load_dotenv()

import os

class Settings:
    def __init__(self):
        self.S3_ENDPOINT = os.getenv("S3_ENDPOINT")
        self.S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
        self.S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
        self.S3_BUCKET = os.getenv("S3_BUCKET")
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.SECRET_KEY = os.getenv("SECRET_KEY")  # <--- add this
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")  # <--- add this, default HS256
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

        missing = [
            var for var, value in [
                ("S3_ENDPOINT", self.S3_ENDPOINT),
                ("S3_ACCESS_KEY", self.S3_ACCESS_KEY),
                ("S3_SECRET_KEY", self.S3_SECRET_KEY),
                ("S3_BUCKET", self.S3_BUCKET),
                ("DATABASE_URL", self.DATABASE_URL),
                ("SECRET_KEY", self.SECRET_KEY),  # <--- required now
            ] if value is None
        ]
        if missing:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

settings = Settings()
