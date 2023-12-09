import sys

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from kafkaHelper import consumeRecord, initConsumer

TOPIC = sys.argv[1]
DB_URI = sys.argv[2]

consumer = initConsumer(TOPIC)

# uri = "mongodb+srv://bakansm:Khanhcool2001@kafkasink.6c3trd5.mongodb.net/?retryWrites=true&w=majority"
uri = sys.argv[2]
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['ViTHSD']
collection = db[TOPIC]

while True:
    records = consumeRecord(consumer)
    for r in records:
        collection.insert_one(r).inserted_id
    