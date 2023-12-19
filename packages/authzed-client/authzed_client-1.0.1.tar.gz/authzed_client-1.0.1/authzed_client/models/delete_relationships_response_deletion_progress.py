from enum import Enum


class DeleteRelationshipsResponseDeletionProgress(str, Enum):
    DELETION_PROGRESS_COMPLETE = "DELETION_PROGRESS_COMPLETE"
    DELETION_PROGRESS_PARTIAL = "DELETION_PROGRESS_PARTIAL"
    DELETION_PROGRESS_UNSPECIFIED = "DELETION_PROGRESS_UNSPECIFIED"

    def __str__(self) -> str:
        return str(self.value)
