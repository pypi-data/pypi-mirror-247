from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_bulk_check_permission_request_item_context import V1BulkCheckPermissionRequestItemContext
    from ..models.v1_object_reference import V1ObjectReference
    from ..models.v1_subject_reference import V1SubjectReference


T = TypeVar("T", bound="V1BulkCheckPermissionRequestItem")


@_attrs_define
class V1BulkCheckPermissionRequestItem:
    """
    Attributes:
        resource (Union[Unset, V1ObjectReference]): ObjectReference is used to refer to a specific object in the system.
        permission (Union[Unset, str]):
        subject (Union[Unset, V1SubjectReference]): SubjectReference is used for referring to the subject portion of a
            Relationship. The relation component is optional and is used for defining a
            sub-relation on the subject, e.g. group:123#members
        context (Union[Unset, V1BulkCheckPermissionRequestItemContext]):
    """

    resource: Union[Unset, "V1ObjectReference"] = UNSET
    permission: Union[Unset, str] = UNSET
    subject: Union[Unset, "V1SubjectReference"] = UNSET
    context: Union[Unset, "V1BulkCheckPermissionRequestItemContext"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        resource: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resource, Unset):
            resource = self.resource.to_dict()

        permission = self.permission
        subject: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.subject, Unset):
            subject = self.subject.to_dict()

        context: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if resource is not UNSET:
            field_dict["resource"] = resource
        if permission is not UNSET:
            field_dict["permission"] = permission
        if subject is not UNSET:
            field_dict["subject"] = subject
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_bulk_check_permission_request_item_context import V1BulkCheckPermissionRequestItemContext
        from ..models.v1_object_reference import V1ObjectReference
        from ..models.v1_subject_reference import V1SubjectReference

        d = src_dict.copy()
        _resource = d.pop("resource", UNSET)
        resource: Union[Unset, V1ObjectReference]
        if isinstance(_resource, Unset):
            resource = UNSET
        else:
            resource = V1ObjectReference.from_dict(_resource)

        permission = d.pop("permission", UNSET)

        _subject = d.pop("subject", UNSET)
        subject: Union[Unset, V1SubjectReference]
        if isinstance(_subject, Unset):
            subject = UNSET
        else:
            subject = V1SubjectReference.from_dict(_subject)

        _context = d.pop("context", UNSET)
        context: Union[Unset, V1BulkCheckPermissionRequestItemContext]
        if isinstance(_context, Unset):
            context = UNSET
        else:
            context = V1BulkCheckPermissionRequestItemContext.from_dict(_context)

        v1_bulk_check_permission_request_item = cls(
            resource=resource,
            permission=permission,
            subject=subject,
            context=context,
        )

        v1_bulk_check_permission_request_item.additional_properties = d
        return v1_bulk_check_permission_request_item

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
