from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_contextualized_caveat import V1ContextualizedCaveat
    from ..models.v1_object_reference import V1ObjectReference
    from ..models.v1_subject_reference import V1SubjectReference


T = TypeVar("T", bound="V1Relationship")


@_attrs_define
class V1Relationship:
    """Relationship specifies how a resource relates to a subject. Relationships
    form the data for the graph over which all permissions questions are
    answered.

        Attributes:
            resource (Union[Unset, V1ObjectReference]): ObjectReference is used to refer to a specific object in the system.
            relation (Union[Unset, str]): relation is how the resource and subject are related.
            subject (Union[Unset, V1SubjectReference]): SubjectReference is used for referring to the subject portion of a
                Relationship. The relation component is optional and is used for defining a
                sub-relation on the subject, e.g. group:123#members
            optional_caveat (Union[Unset, V1ContextualizedCaveat]): ContextualizedCaveat represents a reference to a caveat
                to be used by caveated relationships.
                The context consists of key-value pairs that will be injected at evaluation time.
                The keys must match the arguments defined on the caveat in the schema.
    """

    resource: Union[Unset, "V1ObjectReference"] = UNSET
    relation: Union[Unset, str] = UNSET
    subject: Union[Unset, "V1SubjectReference"] = UNSET
    optional_caveat: Union[Unset, "V1ContextualizedCaveat"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        resource: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resource, Unset):
            resource = self.resource.to_dict()

        relation = self.relation
        subject: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.subject, Unset):
            subject = self.subject.to_dict()

        optional_caveat: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.optional_caveat, Unset):
            optional_caveat = self.optional_caveat.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if resource is not UNSET:
            field_dict["resource"] = resource
        if relation is not UNSET:
            field_dict["relation"] = relation
        if subject is not UNSET:
            field_dict["subject"] = subject
        if optional_caveat is not UNSET:
            field_dict["optionalCaveat"] = optional_caveat

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_contextualized_caveat import V1ContextualizedCaveat
        from ..models.v1_object_reference import V1ObjectReference
        from ..models.v1_subject_reference import V1SubjectReference

        d = src_dict.copy()
        _resource = d.pop("resource", UNSET)
        resource: Union[Unset, V1ObjectReference]
        if isinstance(_resource, Unset):
            resource = UNSET
        else:
            resource = V1ObjectReference.from_dict(_resource)

        relation = d.pop("relation", UNSET)

        _subject = d.pop("subject", UNSET)
        subject: Union[Unset, V1SubjectReference]
        if isinstance(_subject, Unset):
            subject = UNSET
        else:
            subject = V1SubjectReference.from_dict(_subject)

        _optional_caveat = d.pop("optionalCaveat", UNSET)
        optional_caveat: Union[Unset, V1ContextualizedCaveat]
        if isinstance(_optional_caveat, Unset):
            optional_caveat = UNSET
        else:
            optional_caveat = V1ContextualizedCaveat.from_dict(_optional_caveat)

        v1_relationship = cls(
            resource=resource,
            relation=relation,
            subject=subject,
            optional_caveat=optional_caveat,
        )

        v1_relationship.additional_properties = d
        return v1_relationship

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
