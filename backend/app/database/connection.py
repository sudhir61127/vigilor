import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# MongoDB Connection String
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

# Database Name
DATABASE_NAME = os.getenv("DATABASE_NAME", "vigilor")

# Create Mongo Client - with error handling
client = None
database = None

try:
    from pymongo import MongoClient
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
    database = client[DATABASE_NAME]
    # Test connection
    client.server_info()
except Exception as e:
    # Connection failed - database will remain None
    # The application can still run with file-based data
    pass


def get_database():
    """
    Returns the MongoDB database instance.
    Returns None if connection failed (database will use file-based fallbacks).
    """
    return database
