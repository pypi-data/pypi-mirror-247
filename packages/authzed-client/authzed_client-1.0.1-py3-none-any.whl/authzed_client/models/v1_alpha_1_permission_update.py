from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v1_alpha_1_permission_update_permissionship import V1Alpha1PermissionUpdatePermissionship
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_object_reference import V1ObjectReference
    from ..models.v1_subject_reference import V1SubjectReference


T = TypeVar("T", bound="V1Alpha1PermissionUpdate")


@_attrs_define
class V1Alpha1PermissionUpdate:
    """PermissionUpdate represents a single permission update for a specific
    subject's permissions.

        Attributes:
            subject (Union[Unset, V1SubjectReference]): SubjectReference is used for referring to the subject portion of a
                Relationship. The relation component is optional and is used for defining a
                sub-relation on the subject, e.g. group:123#members
            resource (Union[Unset, V1ObjectReference]): ObjectReference is used to refer to a specific object in the system.
            relation (Union[Unset, str]):
            updated_permission (Union[Unset, V1Alpha1PermissionUpdatePermissionship]): todo: work this into the v1 core API
                at some point since it's used
                across services. Default: V1Alpha1PermissionUpdatePermissionship.PERMISSIONSHIP_UNSPECIFIED.
    """

    subject: Union[Unset, "V1SubjectReference"] = UNSET
    resource: Union[Unset, "V1ObjectReference"] = UNSET
    relation: Union[Unset, str] = UNSET
    updated_permission: Union[
        Unset, V1Alpha1PermissionUpdatePermissionship
    ] = V1Alpha1PermissionUpdatePermissionship.PERMISSIONSHIP_UNSPECIFIED
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        subject: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.subject, Unset):
            subject = self.subject.to_dict()

        resource: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resource, Unset):
            resource = self.resource.to_dict()

        relation = self.relation
        updated_permission: Union[Unset, str] = UNSET
        if not isinstance(self.updated_permission, Unset):
            updated_permission = self.updated_permission.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if subject is not UNSET:
            field_dict["subject"] = subject
        if resource is not UNSET:
            field_dict["resource"] = resource
        if relation is not UNSET:
            field_dict["relation"] = relation
        if updated_permission is not UNSET:
            field_dict["updatedPermission"] = updated_permission

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_object_reference import V1ObjectReference
        from ..models.v1_subject_reference import V1SubjectReference

        d = src_dict.copy()
        _subject = d.pop("subject", UNSET)
        subject: Union[Unset, V1SubjectReference]
        if isinstance(_subject, Unset):
            subject = UNSET
        else:
            subject = V1SubjectReference.from_dict(_subject)

        _resource = d.pop("resource", UNSET)
        resource: Union[Unset, V1ObjectReference]
        if isinstance(_resource, Unset):
            resource = UNSET
        else:
            resource = V1ObjectReference.from_dict(_resource)

        relation = d.pop("relation", UNSET)

        _updated_permission = d.pop("updatedPermission", UNSET)
        updated_permission: Union[Unset, V1Alpha1PermissionUpdatePermissionship]
        if isinstance(_updated_permission, Unset):
            updated_permission = UNSET
        else:
            updated_permission = V1Alpha1PermissionUpdatePermissionship(_updated_permission)

        v1_alpha_1_permission_update = cls(
            subject=subject,
            resource=resource,
            relation=relation,
            updated_permission=updated_permission,
        )

        v1_alpha_1_permission_update.additional_properties = d
        return v1_alpha_1_permission_update

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
