from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv('.config')
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.admin_restapi
items_collection = db['items']
clock_in_collection = db['clock_in_records']