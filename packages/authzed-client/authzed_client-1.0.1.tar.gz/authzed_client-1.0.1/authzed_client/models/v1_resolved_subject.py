from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v1_lookup_permissionship import V1LookupPermissionship
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_partial_caveat_info import V1PartialCaveatInfo


T = TypeVar("T", bound="V1ResolvedSubject")


@_attrs_define
class V1ResolvedSubject:
    """ResolvedSubject is a single subject resolved within LookupSubjects.

    Attributes:
        subject_object_id (Union[Unset, str]): subject_object_id is the Object ID of the subject found. May be a `*` if
            a wildcard was found.
        permissionship (Union[Unset, V1LookupPermissionship]): LookupPermissionship represents whether a Lookup response
            was partially evaluated or not Default: V1LookupPermissionship.LOOKUP_PERMISSIONSHIP_UNSPECIFIED.
        partial_caveat_info (Union[Unset, V1PartialCaveatInfo]): PartialCaveatInfo carries information necessary for the
            client to take action
            in the event a response contains a partially evaluated caveat
    """

    subject_object_id: Union[Unset, str] = UNSET
    permissionship: Union[Unset, V1LookupPermissionship] = V1LookupPermissionship.LOOKUP_PERMISSIONSHIP_UNSPECIFIED
    partial_caveat_info: Union[Unset, "V1PartialCaveatInfo"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        subject_object_id = self.subject_object_id
        permissionship: Union[Unset, str] = UNSET
        if not isinstance(self.permissionship, Unset):
            permissionship = self.permissionship.value

        partial_caveat_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.partial_caveat_info, Unset):
            partial_caveat_info = self.partial_caveat_info.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if subject_object_id is not UNSET:
            field_dict["subjectObjectId"] = subject_object_id
        if permissionship is not UNSET:
            field_dict["permissionship"] = permissionship
        if partial_caveat_info is not UNSET:
            field_dict["partialCaveatInfo"] = partial_caveat_info

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_partial_caveat_info import V1PartialCaveatInfo

        d = src_dict.copy()
        subject_object_id = d.pop("subjectObjectId", UNSET)

        _permissionship = d.pop("permissionship", UNSET)
        permissionship: Union[Unset, V1LookupPermissionship]
        if isinstance(_permissionship, Unset):
            permissionship = UNSET
        else:
            permissionship = V1LookupPermissionship(_permissionship)

        _partial_caveat_info = d.pop("partialCaveatInfo", UNSET)
        partial_caveat_info: Union[Unset, V1PartialCaveatInfo]
        if isinstance(_partial_caveat_info, Unset):
            partial_caveat_info = UNSET
        else:
            partial_caveat_info = V1PartialCaveatInfo.from_dict(_partial_caveat_info)

        v1_resolved_subject = cls(
            subject_object_id=subject_object_id,
            permissionship=permissionship,
            partial_caveat_info=partial_caveat_info,
        )

        v1_resolved_subject.additional_properties = d
        return v1_resolved_subject

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
