from abc import ABC, abstractclassmethod
from typing import Any


class BaseSerializer(ABC):
    """
    Base Serializer class from which all other serializers
    must be derived.
    """
    @abstractclassmethod
    def serialize(cls, obj: Any) -> str:
        pass

    @abstractclassmethod
    def deserialize(cls, s: str) -> Any:
        pass
