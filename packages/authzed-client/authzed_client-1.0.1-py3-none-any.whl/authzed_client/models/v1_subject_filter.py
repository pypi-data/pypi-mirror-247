from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.subject_filter_relation_filter import SubjectFilterRelationFilter


T = TypeVar("T", bound="V1SubjectFilter")


@_attrs_define
class V1SubjectFilter:
    """SubjectFilter specifies a filter on the subject of a relationship.

    subject_type is required and all other fields are optional, and will not
    impose any additional requirements if left unspecified.

        Attributes:
            subject_type (Union[Unset, str]):
            optional_subject_id (Union[Unset, str]):
            optional_relation (Union[Unset, SubjectFilterRelationFilter]):
    """

    subject_type: Union[Unset, str] = UNSET
    optional_subject_id: Union[Unset, str] = UNSET
    optional_relation: Union[Unset, "SubjectFilterRelationFilter"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        subject_type = self.subject_type
        optional_subject_id = self.optional_subject_id
        optional_relation: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.optional_relation, Unset):
            optional_relation = self.optional_relation.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if subject_type is not UNSET:
            field_dict["subjectType"] = subject_type
        if optional_subject_id is not UNSET:
            field_dict["optionalSubjectId"] = optional_subject_id
        if optional_relation is not UNSET:
            field_dict["optionalRelation"] = optional_relation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.subject_filter_relation_filter import SubjectFilterRelationFilter

        d = src_dict.copy()
        subject_type = d.pop("subjectType", UNSET)

        optional_subject_id = d.pop("optionalSubjectId", UNSET)

        _optional_relation = d.pop("optionalRelation", UNSET)
        optional_relation: Union[Unset, SubjectFilterRelationFilter]
        if isinstance(_optional_relation, Unset):
            optional_relation = UNSET
        else:
            optional_relation = SubjectFilterRelationFilter.from_dict(_optional_relation)

        v1_subject_filter = cls(
            subject_type=subject_type,
            optional_subject_id=optional_subject_id,
            optional_relation=optional_relation,
        )

        v1_subject_filter.additional_properties = d
        return v1_subject_filter

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
