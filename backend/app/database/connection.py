import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load .env file
load_dotenv()

# MongoDB Connection String
MONGODB_URI = os.getenv("MONGODB_URI")

# Database Name
DATABASE_NAME = os.getenv("DATABASE_NAME", "vigilor")

# Create Mongo Client
client = MongoClient(MONGODB_URI)

# Select Database
database = client[DATABASE_NAME]


def get_database():
    """
    Returns the MongoDB database instance.
    """
    return database