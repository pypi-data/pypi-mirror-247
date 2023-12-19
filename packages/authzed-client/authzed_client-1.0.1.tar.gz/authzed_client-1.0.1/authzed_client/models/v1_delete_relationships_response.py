from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.delete_relationships_response_deletion_progress import DeleteRelationshipsResponseDeletionProgress
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_zed_token import V1ZedToken


T = TypeVar("T", bound="V1DeleteRelationshipsResponse")


@_attrs_define
class V1DeleteRelationshipsResponse:
    """
    Attributes:
        deleted_at (Union[Unset, V1ZedToken]): ZedToken is used to provide causality metadata between Write and Check
            requests.

            See the authzed.api.v1.Consistency message for more information.
        deletion_progress (Union[Unset, DeleteRelationshipsResponseDeletionProgress]):  - DELETION_PROGRESS_COMPLETE:
            DELETION_PROGRESS_COMPLETE indicates that all remaining relationships matching the filter
            were deleted. Will be returned even if no relationships were deleted.
             - DELETION_PROGRESS_PARTIAL: DELETION_PROGRESS_PARTIAL indicates that a subset of the relationships matching
            the filter
            were deleted. Only returned if optional_allow_partial_deletions was true, an optional_limit was
            specified, and there existed more relationships matching the filter than optional_limit would allow.
            Once all remaining relationships have been deleted, DELETION_PROGRESS_COMPLETE will be returned. Default:
            DeleteRelationshipsResponseDeletionProgress.DELETION_PROGRESS_UNSPECIFIED.
    """

    deleted_at: Union[Unset, "V1ZedToken"] = UNSET
    deletion_progress: Union[
        Unset, DeleteRelationshipsResponseDeletionProgress
    ] = DeleteRelationshipsResponseDeletionProgress.DELETION_PROGRESS_UNSPECIFIED
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        deleted_at: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.deleted_at, Unset):
            deleted_at = self.deleted_at.to_dict()

        deletion_progress: Union[Unset, str] = UNSET
        if not isinstance(self.deletion_progress, Unset):
            deletion_progress = self.deletion_progress.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if deleted_at is not UNSET:
            field_dict["deletedAt"] = deleted_at
        if deletion_progress is not UNSET:
            field_dict["deletionProgress"] = deletion_progress

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_zed_token import V1ZedToken

        d = src_dict.copy()
        _deleted_at = d.pop("deletedAt", UNSET)
        deleted_at: Union[Unset, V1ZedToken]
        if isinstance(_deleted_at, Unset):
            deleted_at = UNSET
        else:
            deleted_at = V1ZedToken.from_dict(_deleted_at)

        _deletion_progress = d.pop("deletionProgress", UNSET)
        deletion_progress: Union[Unset, DeleteRelationshipsResponseDeletionProgress]
        if isinstance(_deletion_progress, Unset):
            deletion_progress = UNSET
        else:
            deletion_progress = DeleteRelationshipsResponseDeletionProgress(_deletion_progress)

        v1_delete_relationships_response = cls(
            deleted_at=deleted_at,
            deletion_progress=deletion_progress,
        )

        v1_delete_relationships_response.additional_properties = d
        return v1_delete_relationships_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
