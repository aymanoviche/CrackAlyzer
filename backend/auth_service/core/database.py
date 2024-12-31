from pymongo import MongoClient
from pymongo.server_api import ServerApi
import pymongo
from backend.auth_service.core.config import get_settings

settings = get_settings()

client = client = MongoClient(settings.DATABASE_URL, server_api=ServerApi('1'))
print('Connected to MongoDB...')

db = client[settings.MONGO_INITDB_DATABASE]
User = db.users

# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

def get_db():
    # try:
    yield db
    # finally:
    #     client.close()