from typing import Any

import msgpack

from .baseserializer import BaseSerializer


class MsgPackSerializer(BaseSerializer):
    def serialize(cls, obj: Any) -> str:
        return msgpack.dumps(obj)

    def deserialize(cls, s: str) -> Any:
        return msgpack.loads(s)
