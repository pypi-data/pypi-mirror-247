from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_subject_filter import V1SubjectFilter


T = TypeVar("T", bound="V1RelationshipFilter")


@_attrs_define
class V1RelationshipFilter:
    """RelationshipFilter is a collection of filters which when applied to a
    relationship will return relationships that have exactly matching fields.

    resource_type is required. All other fields are optional and if left
    unspecified will not filter relationships.

        Attributes:
            resource_type (Union[Unset, str]):
            optional_resource_id (Union[Unset, str]):
            optional_relation (Union[Unset, str]):
            optional_subject_filter (Union[Unset, V1SubjectFilter]): SubjectFilter specifies a filter on the subject of a
                relationship.

                subject_type is required and all other fields are optional, and will not
                impose any additional requirements if left unspecified.
    """

    resource_type: Union[Unset, str] = UNSET
    optional_resource_id: Union[Unset, str] = UNSET
    optional_relation: Union[Unset, str] = UNSET
    optional_subject_filter: Union[Unset, "V1SubjectFilter"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        resource_type = self.resource_type
        optional_resource_id = self.optional_resource_id
        optional_relation = self.optional_relation
        optional_subject_filter: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.optional_subject_filter, Unset):
            optional_subject_filter = self.optional_subject_filter.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if resource_type is not UNSET:
            field_dict["resourceType"] = resource_type
        if optional_resource_id is not UNSET:
            field_dict["optionalResourceId"] = optional_resource_id
        if optional_relation is not UNSET:
            field_dict["optionalRelation"] = optional_relation
        if optional_subject_filter is not UNSET:
            field_dict["optionalSubjectFilter"] = optional_subject_filter

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_subject_filter import V1SubjectFilter

        d = src_dict.copy()
        resource_type = d.pop("resourceType", UNSET)

        optional_resource_id = d.pop("optionalResourceId", UNSET)

        optional_relation = d.pop("optionalRelation", UNSET)

        _optional_subject_filter = d.pop("optionalSubjectFilter", UNSET)
        optional_subject_filter: Union[Unset, V1SubjectFilter]
        if isinstance(_optional_subject_filter, Unset):
            optional_subject_filter = UNSET
        else:
            optional_subject_filter = V1SubjectFilter.from_dict(_optional_subject_filter)

        v1_relationship_filter = cls(
            resource_type=resource_type,
            optional_resource_id=optional_resource_id,
            optional_relation=optional_relation,
            optional_subject_filter=optional_subject_filter,
        )

        v1_relationship_filter.additional_properties = d
        return v1_relationship_filter

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
