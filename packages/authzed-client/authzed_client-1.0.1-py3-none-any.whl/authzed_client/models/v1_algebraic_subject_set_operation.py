from enum import Enum


class V1AlgebraicSubjectSetOperation(str, Enum):
    OPERATION_EXCLUSION = "OPERATION_EXCLUSION"
    OPERATION_INTERSECTION = "OPERATION_INTERSECTION"
    OPERATION_UNION = "OPERATION_UNION"
    OPERATION_UNSPECIFIED = "OPERATION_UNSPECIFIED"

    def __str__(self) -> str:
        return str(self.value)
