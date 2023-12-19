from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_permission_relationship_tree import V1PermissionRelationshipTree
    from ..models.v1_zed_token import V1ZedToken


T = TypeVar("T", bound="V1ExpandPermissionTreeResponse")


@_attrs_define
class V1ExpandPermissionTreeResponse:
    """
    Attributes:
        expanded_at (Union[Unset, V1ZedToken]): ZedToken is used to provide causality metadata between Write and Check
            requests.

            See the authzed.api.v1.Consistency message for more information.
        tree_root (Union[Unset, V1PermissionRelationshipTree]): PermissionRelationshipTree is used for representing a
            tree of a resource and
            its permission relationships with other objects.
    """

    expanded_at: Union[Unset, "V1ZedToken"] = UNSET
    tree_root: Union[Unset, "V1PermissionRelationshipTree"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        expanded_at: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.expanded_at, Unset):
            expanded_at = self.expanded_at.to_dict()

        tree_root: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tree_root, Unset):
            tree_root = self.tree_root.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if expanded_at is not UNSET:
            field_dict["expandedAt"] = expanded_at
        if tree_root is not UNSET:
            field_dict["treeRoot"] = tree_root

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_permission_relationship_tree import V1PermissionRelationshipTree
        from ..models.v1_zed_token import V1ZedToken

        d = src_dict.copy()
        _expanded_at = d.pop("expandedAt", UNSET)
        expanded_at: Union[Unset, V1ZedToken]
        if isinstance(_expanded_at, Unset):
            expanded_at = UNSET
        else:
            expanded_at = V1ZedToken.from_dict(_expanded_at)

        _tree_root = d.pop("treeRoot", UNSET)
        tree_root: Union[Unset, V1PermissionRelationshipTree]
        if isinstance(_tree_root, Unset):
            tree_root = UNSET
        else:
            tree_root = V1PermissionRelationshipTree.from_dict(_tree_root)

        v1_expand_permission_tree_response = cls(
            expanded_at=expanded_at,
            tree_root=tree_root,
        )

        v1_expand_permission_tree_response.additional_properties = d
        return v1_expand_permission_tree_response

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
