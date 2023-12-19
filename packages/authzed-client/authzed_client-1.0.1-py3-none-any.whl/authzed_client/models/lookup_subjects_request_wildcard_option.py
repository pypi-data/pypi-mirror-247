from enum import Enum


class LookupSubjectsRequestWildcardOption(str, Enum):
    WILDCARD_OPTION_EXCLUDE_WILDCARDS = "WILDCARD_OPTION_EXCLUDE_WILDCARDS"
    WILDCARD_OPTION_INCLUDE_WILDCARDS = "WILDCARD_OPTION_INCLUDE_WILDCARDS"
    WILDCARD_OPTION_UNSPECIFIED = "WILDCARD_OPTION_UNSPECIFIED"

    def __str__(self) -> str:
        return str(self.value)
