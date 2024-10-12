from pymongo import MongoClient
import os

client = MongoClient("mongodb+srv://test:1234@masterapi.q2jxd.mongodb.net/?retryWrites=true&w=majority&appName=masterapi")
db = client.admin_restapi
items_collection = db['items']
clock_in_collection = db['clock_in_records']