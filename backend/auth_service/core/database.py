from pymongo import MongoClient
from pymongo.server_api import ServerApi
import pymongo
from backend.auth_service.core.config import get_settings

settings = get_settings()

client = client = MongoClient(settings.DATABASE_URL, server_api=ServerApi('1'))
print('Connected to MongoDB...')

db = client[settings.MONGO_INITDB_DATABASE]
User = db.users
PasswordAnalyzeHistory = db.password_analyze_history
BreachHistory = db.breach_history
PasswordCrackerHistory = db.password_cracker_history

def get_db():
    yield db