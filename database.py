from pymongo import MongoClient # type: ignore
from pymongo.errors import ServerSelectionTimeoutError # type: ignore
import certifi

MONGO_URL = "mongodb+srv://deepakcool2003:Deepak2003@deepak-mittal.nno35.mongodb.net/?retryWrites=true&w=majority&appName=deepak-mittal"
client = MongoClient(MONGO_URL, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
db = client["students_db"]
students_collection = db["students"]

