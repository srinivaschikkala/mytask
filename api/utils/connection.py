import pika
from os import environ
from pymongo import MongoClient

def get_rabbitmq_connection():
    parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(parameters)
    return connection 




def get_mongodb_collection():
    print(environ.get("MONGODB_DATABASE"))
    client = MongoClient(environ.get("MONGODB_URI",))
    db = client[environ.get("MONGODB_DATABASE")]
    collection = db[environ.get("MONGODB_COLLECTION")]
    return collection