from enum import Enum


class DeveloperErrorSource(str, Enum):
    ASSERTION = "ASSERTION"
    CHECK_WATCH = "CHECK_WATCH"
    RELATIONSHIP = "RELATIONSHIP"
    SCHEMA = "SCHEMA"
    UNKNOWN_SOURCE = "UNKNOWN_SOURCE"
    VALIDATION_YAML = "VALIDATION_YAML"

    def __str__(self) -> str:
        return str(self.value)
