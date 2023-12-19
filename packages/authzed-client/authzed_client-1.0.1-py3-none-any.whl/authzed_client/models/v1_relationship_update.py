from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v1_relationship_update_operation import V1RelationshipUpdateOperation
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_relationship import V1Relationship


T = TypeVar("T", bound="V1RelationshipUpdate")


@_attrs_define
class V1RelationshipUpdate:
    """RelationshipUpdate is used for mutating a single relationship within the
    service.

    CREATE will create the relationship only if it doesn't exist, and error
    otherwise.

    TOUCH will upsert the relationship, and will not error if it
    already exists.

    DELETE will delete the relationship. If the relationship does not exist,
    this operation will no-op.

        Attributes:
            operation (Union[Unset, V1RelationshipUpdateOperation]):  Default:
                V1RelationshipUpdateOperation.OPERATION_UNSPECIFIED.
            relationship (Union[Unset, V1Relationship]): Relationship specifies how a resource relates to a subject.
                Relationships
                form the data for the graph over which all permissions questions are
                answered.
    """

    operation: Union[Unset, V1RelationshipUpdateOperation] = V1RelationshipUpdateOperation.OPERATION_UNSPECIFIED
    relationship: Union[Unset, "V1Relationship"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        operation: Union[Unset, str] = UNSET
        if not isinstance(self.operation, Unset):
            operation = self.operation.value

        relationship: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.relationship, Unset):
            relationship = self.relationship.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if operation is not UNSET:
            field_dict["operation"] = operation
        if relationship is not UNSET:
            field_dict["relationship"] = relationship

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_relationship import V1Relationship

        d = src_dict.copy()
        _operation = d.pop("operation", UNSET)
        operation: Union[Unset, V1RelationshipUpdateOperation]
        if isinstance(_operation, Unset):
            operation = UNSET
        else:
            operation = V1RelationshipUpdateOperation(_operation)

        _relationship = d.pop("relationship", UNSET)
        relationship: Union[Unset, V1Relationship]
        if isinstance(_relationship, Unset):
            relationship = UNSET
        else:
            relationship = V1Relationship.from_dict(_relationship)

        v1_relationship_update = cls(
            operation=operation,
            relationship=relationship,
        )

        v1_relationship_update.additional_properties = d
        return v1_relationship_update

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
