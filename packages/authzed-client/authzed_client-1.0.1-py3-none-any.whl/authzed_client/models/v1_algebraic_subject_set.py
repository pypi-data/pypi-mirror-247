from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v1_algebraic_subject_set_operation import V1AlgebraicSubjectSetOperation
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_permission_relationship_tree import V1PermissionRelationshipTree


T = TypeVar("T", bound="V1AlgebraicSubjectSet")


@_attrs_define
class V1AlgebraicSubjectSet:
    """AlgebraicSubjectSet is a subject set which is computed based on applying the
    specified operation to the operands according to the algebra of sets.

    UNION is a logical set containing the subject members from all operands.

    INTERSECTION is a logical set containing only the subject members which are
    present in all operands.

    EXCLUSION is a logical set containing only the subject members which are
    present in the first operand, and none of the other operands.

        Attributes:
            operation (Union[Unset, V1AlgebraicSubjectSetOperation]):  Default:
                V1AlgebraicSubjectSetOperation.OPERATION_UNSPECIFIED.
            children (Union[Unset, List['V1PermissionRelationshipTree']]):
    """

    operation: Union[Unset, V1AlgebraicSubjectSetOperation] = V1AlgebraicSubjectSetOperation.OPERATION_UNSPECIFIED
    children: Union[Unset, List["V1PermissionRelationshipTree"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        operation: Union[Unset, str] = UNSET
        if not isinstance(self.operation, Unset):
            operation = self.operation.value

        children: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.children, Unset):
            children = []
            for children_item_data in self.children:
                children_item = children_item_data.to_dict()

                children.append(children_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if operation is not UNSET:
            field_dict["operation"] = operation
        if children is not UNSET:
            field_dict["children"] = children

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_permission_relationship_tree import V1PermissionRelationshipTree

        d = src_dict.copy()
        _operation = d.pop("operation", UNSET)
        operation: Union[Unset, V1AlgebraicSubjectSetOperation]
        if isinstance(_operation, Unset):
            operation = UNSET
        else:
            operation = V1AlgebraicSubjectSetOperation(_operation)

        children = []
        _children = d.pop("children", UNSET)
        for children_item_data in _children or []:
            children_item = V1PermissionRelationshipTree.from_dict(children_item_data)

            children.append(children_item)

        v1_algebraic_subject_set = cls(
            operation=operation,
            children=children,
        )

        v1_algebraic_subject_set.additional_properties = d
        return v1_algebraic_subject_set

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
