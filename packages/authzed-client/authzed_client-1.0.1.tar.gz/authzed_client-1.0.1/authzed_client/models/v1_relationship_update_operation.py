from enum import Enum


class V1RelationshipUpdateOperation(str, Enum):
    OPERATION_CREATE = "OPERATION_CREATE"
    OPERATION_DELETE = "OPERATION_DELETE"
    OPERATION_TOUCH = "OPERATION_TOUCH"
    OPERATION_UNSPECIFIED = "OPERATION_UNSPECIFIED"

    def __str__(self) -> str:
        return str(self.value)
