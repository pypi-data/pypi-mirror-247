from enum import Enum


class V1Alpha1PermissionUpdatePermissionship(str, Enum):
    PERMISSIONSHIP_HAS_PERMISSION = "PERMISSIONSHIP_HAS_PERMISSION"
    PERMISSIONSHIP_NO_PERMISSION = "PERMISSIONSHIP_NO_PERMISSION"
    PERMISSIONSHIP_UNSPECIFIED = "PERMISSIONSHIP_UNSPECIFIED"

    def __str__(self) -> str:
        return str(self.value)
