from pymongo import MongoClient
from django.conf import settings
from bson.objectid import ObjectId


client = MongoClient(settings.MONGODB_HOST, int(settings.MONGODB_PORT))
db = client[settings.MONGODB_DB_NAME]
collection = db['salon_pictures']


def save_picture_to_mongodb(picture_data):
    return collection.insert_one({'picture_data': picture_data}).inserted_id

    
def get_picture_from_mongodb(salon_id):
    salon_picture = collection.find_one({'_id': ObjectId(salon_id)})
    if salon_picture:
        return salon_picture['picture_data']
    return None


def delete_picture_from_mongodb(salon_id):
    collection.delete_one({'_id': ObjectId(salon_id)})