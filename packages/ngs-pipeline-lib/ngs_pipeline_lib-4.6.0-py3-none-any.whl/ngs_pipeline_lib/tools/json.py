import json
from datetime import datetime
from pathlib import Path


# extend the json.JSONEncoder class
class NGSJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # datetime object are encoded as ISO 8601
        if isinstance(obj, datetime):
            return obj.isoformat(timespec="milliseconds").replace("+00:00", "Z")
        elif isinstance(obj, Path):
            return str(obj)

        return json.JSONEncoder.default(self, obj)
