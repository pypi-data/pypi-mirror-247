import bjson
from typing import Any

from .baseserializer import BaseSerializer


class BJsonSerializer(BaseSerializer):
    """
    BJson Serializer
    """
    def serialize(cls, obj: Any) -> str:
        return bjson.dumps(obj)

    def deserialize(cls, s: str) -> Any:
        return bjson.loads(s)
