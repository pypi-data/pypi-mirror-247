from typing import Any

import yaml

from .baseserializer import BaseSerializer


class YamlSerializer(BaseSerializer):
    """
    YAML serializer
    """
    def serialize(cls, obj: Any) -> str:
        return yaml.safe_dump(obj)

    def deserialize(cls, s: str) -> Any:
        return yaml.safe_load(s)
