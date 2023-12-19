from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0_developer_error import V0DeveloperError
    from ..models.v0_relation_tuple import V0RelationTuple


T = TypeVar("T", bound="V0EditCheckResult")


@_attrs_define
class V0EditCheckResult:
    """
    Attributes:
        relationship (Union[Unset, V0RelationTuple]):
        is_member (Union[Unset, bool]):
        error (Union[Unset, V0DeveloperError]):
    """

    relationship: Union[Unset, "V0RelationTuple"] = UNSET
    is_member: Union[Unset, bool] = UNSET
    error: Union[Unset, "V0DeveloperError"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        relationship: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.relationship, Unset):
            relationship = self.relationship.to_dict()

        is_member = self.is_member
        error: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if relationship is not UNSET:
            field_dict["relationship"] = relationship
        if is_member is not UNSET:
            field_dict["isMember"] = is_member
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v0_developer_error import V0DeveloperError
        from ..models.v0_relation_tuple import V0RelationTuple

        d = src_dict.copy()
        _relationship = d.pop("relationship", UNSET)
        relationship: Union[Unset, V0RelationTuple]
        if isinstance(_relationship, Unset):
            relationship = UNSET
        else:
            relationship = V0RelationTuple.from_dict(_relationship)

        is_member = d.pop("isMember", UNSET)

        _error = d.pop("error", UNSET)
        error: Union[Unset, V0DeveloperError]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = V0DeveloperError.from_dict(_error)

        v0_edit_check_result = cls(
            relationship=relationship,
            is_member=is_member,
            error=error,
        )

        v0_edit_check_result.additional_properties = d
        return v0_edit_check_result

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
