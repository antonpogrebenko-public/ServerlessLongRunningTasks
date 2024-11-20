import json
from datetime import datetime, date
from bson import ObjectId


class MongoDBJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for MongoDB ObjectId and datetime objects
    """
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)