from enum import Enum


class V1PreconditionOperation(str, Enum):
    OPERATION_MUST_MATCH = "OPERATION_MUST_MATCH"
    OPERATION_MUST_NOT_MATCH = "OPERATION_MUST_NOT_MATCH"
    OPERATION_UNSPECIFIED = "OPERATION_UNSPECIFIED"

    def __str__(self) -> str:
        return str(self.value)
