import json
from datetime import datetime


class EventBase(object):
    environment_aware = True

    def __init__(self):
        self.event_timestamp_utc = datetime.utcnow()

    def serialize(self):
        return json.dumps(self.__dict__, cls=DateTimeEncoder)

    def deserialize(self, json_body):
        self.__dict__ = json.loads(json_body)

''' Custom encoder needed to overcome the problem of json.dumps
    not able to handle datetime types.
'''
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)
