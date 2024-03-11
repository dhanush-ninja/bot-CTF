from datetime import datetime
from mongogettersetter import MongoGetterSetter
from src.Database import Database

db = Database.get_connection()
channels = db.channels  # This collection will store channel creation and deletion records

class ChannelCollection(metaclass=MongoGetterSetter):
    def __init__(self, channel_name):
        self._collection = db.channels
        self._filter_query = {
            "channel_name": channel_name
        }

class Channel:
    def __init__(self, channel_name):
        self.collection = ChannelCollection(channel_name)
        self.channel_name = channel_name

    @staticmethod
    def record_channel_creation(channel_name, creator_username, role_name,status):
        try:
            # Create a record for the new channel
            channel_document = {
                "channel_name": channel_name,
                "creator_username": creator_username,
                "role_name": role_name,
                "operation": "create",
                "status":status,
                "timestamp": datetime.utcnow()
            }

            db.channels.insert_one(channel_document)
            
            return {
                "status": 200,
                "message": "Channel creation recorded successfully"
            }

        except Exception as e:
            return {
                "status": 400,
                "message": str(e)
            }

    @staticmethod
    def record_channel_deletion(channel_name, deleter_username):
        try:
            # Create a record for the deleted channel
            channel_document = {
                "channel_name": channel_name,
                "deleter_username": deleter_username,
                "operation": "delete",
                "timestamp": datetime.utcnow()
            }

            db.channels.insert_one(channel_document)
            
            return {
                "status": 200,
                "message": "Channel deletion recorded successfully"
            }

        except Exception as e:
            return {
                "status": 400,
                "message": str(e)
            }
