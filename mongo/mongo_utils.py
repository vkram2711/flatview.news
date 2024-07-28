import os

from mongoengine import connect
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

MONGO_DB_USERNAME = os.getenv('MONGO_DB_USERNAME')
MONGO_DB_PASSWORD = os.getenv('MONGO_DB_PASSWORD')
MONGO_DB_CLUSTER = os.getenv('MONGO_DB_CLUSTER')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')

uri = f"mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@{MONGO_DB_CLUSTER}.hfggwmb.mongodb.net/?retryWrites=true&w=majority&appName={MONGO_DB_NAME}"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


connect(host=uri)
