from datetime import time
from datetime import datetime
from datetime import timedelta
import json
import enum


def to_serializable(val):
    """JSON serializer for objects not serializable by default"""""

    if isinstance(val):
        return val.isoformat()
    elif isinstance(val, enum.Enum):
        return val.value
    elif hasattr(val, '__dict__'):
        return val.__dict__
    return val


def to_json(data):
    """Converts object to JSON formatted string"""""

    return json.dumps(data, default=to_serializable)
    """"
    """
