from bson import ObjectId
from datetime import datetime


def convert_mongo_obj(doc):
    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key] = value.isoformat()
        elif isinstance(value, ObjectId):
            doc[key] = str(value)
        elif isinstance(value, dict):
            doc[key] = convert_mongo_obj(value)
    return doc
