from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_consistency import V1Consistency
    from ..models.v1_object_reference import V1ObjectReference


T = TypeVar("T", bound="V1ExpandPermissionTreeRequest")


@_attrs_define
class V1ExpandPermissionTreeRequest:
    """ExpandPermissionTreeRequest returns a tree representing the expansion of all
    relationships found accessible from a permission or relation on a particular
    resource.

    ExpandPermissionTreeRequest is typically used to determine the full set of
    subjects with a permission, along with the relationships that grant said
    access.

        Attributes:
            consistency (Union[Unset, V1Consistency]): Consistency will define how a request is handled by the backend.
                By defining a consistency requirement, and a token at which those
                requirements should be applied, where applicable.
            resource (Union[Unset, V1ObjectReference]): ObjectReference is used to refer to a specific object in the system.
            permission (Union[Unset, str]): permission is the name of the permission or relation over which to run the
                expansion for the resource.
    """

    consistency: Union[Unset, "V1Consistency"] = UNSET
    resource: Union[Unset, "V1ObjectReference"] = UNSET
    permission: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        consistency: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.consistency, Unset):
            consistency = self.consistency.to_dict()

        resource: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resource, Unset):
            resource = self.resource.to_dict()

        permission = self.permission

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if consistency is not UNSET:
            field_dict["consistency"] = consistency
        if resource is not UNSET:
            field_dict["resource"] = resource
        if permission is not UNSET:
            field_dict["permission"] = permission

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_consistency import V1Consistency
        from ..models.v1_object_reference import V1ObjectReference

        d = src_dict.copy()
        _consistency = d.pop("consistency", UNSET)
        consistency: Union[Unset, V1Consistency]
        if isinstance(_consistency, Unset):
            consistency = UNSET
        else:
            consistency = V1Consistency.from_dict(_consistency)

        _resource = d.pop("resource", UNSET)
        resource: Union[Unset, V1ObjectReference]
        if isinstance(_resource, Unset):
            resource = UNSET
        else:
            resource = V1ObjectReference.from_dict(_resource)

        permission = d.pop("permission", UNSET)

        v1_expand_permission_tree_request = cls(
            consistency=consistency,
            resource=resource,
            permission=permission,
        )

        v1_expand_permission_tree_request.additional_properties = d
        return v1_expand_permission_tree_request

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
