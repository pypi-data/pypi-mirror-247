import json
from typing import Any

from .baseserializer import BaseSerializer


class JsonSerializer(BaseSerializer):
    """
    JSON Serializer
    """
    def serialize(cls, obj: Any) -> str:
        return json.dumps(obj)

    def deserialize(cls, s: str) -> Any:
        return json.loads(s)
