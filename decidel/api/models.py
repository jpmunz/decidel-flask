import uuid
import json
from flask import abort
from decidel.db import redis_store


class DecidelModel(object):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": "https://decidels.ca/schemas/decidel.json",
        "description": "An object that encapsulates making a decision among a group of friends",
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "title": {"type": "string"},
            "options": {
                "type": "array",
                "minItems": 2,
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "isRemoved": {"type": "boolean"},
                    },
                    "required": ["title"],
                    "additionalProperties": False,
                },
            },
            "deciders": {
                "type": "array",
                "minItems": 2,
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "isNext": {"type": "boolean"},
                    },
                    "required": ["name"],
                    "additionalProperties": False,
                },
            },
            "history": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "userName": {"type": "string"},
                        "title": {"type": "string"},
                        "action": {"type": "string", "enum": ["ADDED", "REMOVED"]},
                    },
                    "required": ["userName", "title", "action"],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["title", "options", "deciders", "history"],
        "additionalProperties": False,
    }

    @staticmethod
    def key(id):
        return "decidels:{}".format(id)

    @staticmethod
    def get_or_404(id):
        stored_value = redis_store.get(DecidelModel.key(id))

        if not stored_value:
            abort(404)

        return DecidelModel(stored_value)

    @staticmethod
    def create(from_json):
        id = uuid.uuid4().hex
        from_json["id"] = id

        stored_value = json.dumps(from_json)
        redis_store.set(DecidelModel.key(id), stored_value)

        return DecidelModel(stored_value)

    def __init__(self, stored_value):
        self.stored_value = stored_value

    def update(self, from_json):
        current = self.as_json()
        current.update(from_json)

        self.stored_value = json.dumps(current)
        redis_store.set(DecidelModel.key(self.as_json()["id"]), self.stored_value)

        return self

    def as_json(self):
        return json.loads(self.stored_value)
