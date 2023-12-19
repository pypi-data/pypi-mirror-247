from enum import Enum


class LookupShareResponseLookupStatus(str, Enum):
    FAILED_TO_LOOKUP = "FAILED_TO_LOOKUP"
    UNKNOWN_REFERENCE = "UNKNOWN_REFERENCE"
    UPGRADED_REFERENCE = "UPGRADED_REFERENCE"
    VALID_REFERENCE = "VALID_REFERENCE"

    def __str__(self) -> str:
        return str(self.value)
