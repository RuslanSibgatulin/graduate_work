import os


POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
POSTGRES_DB = os.getenv("POSTGRES_DB", "movies")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_POST = os.getenv("MONGO_POST", 27017)
MONGO_DB = os.getenv("MONGO_DB", "like")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "profiles")
MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_POST}/"
REAL_USER_UUID = "908e33da-6f57-40a5-a8cf-5722dbeed1dc"  # Your real user_id in auth db


GENRES_COUNT = [2, 3, 4]