from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_algebraic_subject_set import V1AlgebraicSubjectSet
    from ..models.v1_direct_subject_set import V1DirectSubjectSet
    from ..models.v1_object_reference import V1ObjectReference


T = TypeVar("T", bound="V1PermissionRelationshipTree")


@_attrs_define
class V1PermissionRelationshipTree:
    """PermissionRelationshipTree is used for representing a tree of a resource and
    its permission relationships with other objects.

        Attributes:
            intermediate (Union[Unset, V1AlgebraicSubjectSet]): AlgebraicSubjectSet is a subject set which is computed based
                on applying the
                specified operation to the operands according to the algebra of sets.

                UNION is a logical set containing the subject members from all operands.

                INTERSECTION is a logical set containing only the subject members which are
                present in all operands.

                EXCLUSION is a logical set containing only the subject members which are
                present in the first operand, and none of the other operands.
            leaf (Union[Unset, V1DirectSubjectSet]): DirectSubjectSet is a subject set which is simply a collection of
                subjects.
            expanded_object (Union[Unset, V1ObjectReference]): ObjectReference is used to refer to a specific object in the
                system.
            expanded_relation (Union[Unset, str]):
    """

    intermediate: Union[Unset, "V1AlgebraicSubjectSet"] = UNSET
    leaf: Union[Unset, "V1DirectSubjectSet"] = UNSET
    expanded_object: Union[Unset, "V1ObjectReference"] = UNSET
    expanded_relation: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        intermediate: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.intermediate, Unset):
            intermediate = self.intermediate.to_dict()

        leaf: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.leaf, Unset):
            leaf = self.leaf.to_dict()

        expanded_object: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.expanded_object, Unset):
            expanded_object = self.expanded_object.to_dict()

        expanded_relation = self.expanded_relation

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if intermediate is not UNSET:
            field_dict["intermediate"] = intermediate
        if leaf is not UNSET:
            field_dict["leaf"] = leaf
        if expanded_object is not UNSET:
            field_dict["expandedObject"] = expanded_object
        if expanded_relation is not UNSET:
            field_dict["expandedRelation"] = expanded_relation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_algebraic_subject_set import V1AlgebraicSubjectSet
        from ..models.v1_direct_subject_set import V1DirectSubjectSet
        from ..models.v1_object_reference import V1ObjectReference

        d = src_dict.copy()
        _intermediate = d.pop("intermediate", UNSET)
        intermediate: Union[Unset, V1AlgebraicSubjectSet]
        if isinstance(_intermediate, Unset):
            intermediate = UNSET
        else:
            intermediate = V1AlgebraicSubjectSet.from_dict(_intermediate)

        _leaf = d.pop("leaf", UNSET)
        leaf: Union[Unset, V1DirectSubjectSet]
        if isinstance(_leaf, Unset):
            leaf = UNSET
        else:
            leaf = V1DirectSubjectSet.from_dict(_leaf)

        _expanded_object = d.pop("expandedObject", UNSET)
        expanded_object: Union[Unset, V1ObjectReference]
        if isinstance(_expanded_object, Unset):
            expanded_object = UNSET
        else:
            expanded_object = V1ObjectReference.from_dict(_expanded_object)

        expanded_relation = d.pop("expandedRelation", UNSET)

        v1_permission_relationship_tree = cls(
            intermediate=intermediate,
            leaf=leaf,
            expanded_object=expanded_object,
            expanded_relation=expanded_relation,
        )

        v1_permission_relationship_tree.additional_properties = d
        return v1_permission_relationship_tree

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
