from database import mongoDB


log_schema = {
    'validator': {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["timestamp", "alertType", "description","cameraId"],
            "properties": {
                "timestamp": {
                    "bsonType": "date",
                    "description": "Date and time when the alert occurred."
                },
                "alertType": {
                    "bsonType": "string",
                    "description": "Type of alert."
                },
                "description": {
                    "bsonType": "string",
                    "description": "Description of the alert."
                },
                "cameraId": {
                    "bsonType": "string",
                    "description": "ID of the camera or monitoring device."
                },
            }
        }
    }
}

if 'logs' not in mongoDB.list_collection_names():
    logs_collection = mongoDB.create_collection('logs', validator=log_schema['validator'])
else:
    logs_collection = mongoDB['logs']