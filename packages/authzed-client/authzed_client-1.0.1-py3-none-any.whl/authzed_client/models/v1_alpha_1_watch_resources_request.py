from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_zed_token import V1ZedToken


T = TypeVar("T", bound="V1Alpha1WatchResourcesRequest")


@_attrs_define
class V1Alpha1WatchResourcesRequest:
    """WatchResourcesRequest starts a watch for specific permission updates
    for the given resource and subject types.

        Attributes:
            resource_object_type (Union[Unset, str]): resource_object_type is the type of resource object for which we will
                watch for changes.
            permission (Union[Unset, str]): permission is the name of the permission or relation for which we will
                watch for changes.
            subject_object_type (Union[Unset, str]): subject_object_type is the type of the subject resource for which we
                will
                watch for changes.
            optional_subject_relation (Union[Unset, str]): optional_subject_relation allows you to specify a group of
                subjects to watch
                for a given subject type.
            optional_start_cursor (Union[Unset, V1ZedToken]): ZedToken is used to provide causality metadata between Write
                and Check
                requests.

                See the authzed.api.v1.Consistency message for more information.
    """

    resource_object_type: Union[Unset, str] = UNSET
    permission: Union[Unset, str] = UNSET
    subject_object_type: Union[Unset, str] = UNSET
    optional_subject_relation: Union[Unset, str] = UNSET
    optional_start_cursor: Union[Unset, "V1ZedToken"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        resource_object_type = self.resource_object_type
        permission = self.permission
        subject_object_type = self.subject_object_type
        optional_subject_relation = self.optional_subject_relation
        optional_start_cursor: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.optional_start_cursor, Unset):
            optional_start_cursor = self.optional_start_cursor.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if resource_object_type is not UNSET:
            field_dict["resourceObjectType"] = resource_object_type
        if permission is not UNSET:
            field_dict["permission"] = permission
        if subject_object_type is not UNSET:
            field_dict["subjectObjectType"] = subject_object_type
        if optional_subject_relation is not UNSET:
            field_dict["optionalSubjectRelation"] = optional_subject_relation
        if optional_start_cursor is not UNSET:
            field_dict["optionalStartCursor"] = optional_start_cursor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_zed_token import V1ZedToken

        d = src_dict.copy()
        resource_object_type = d.pop("resourceObjectType", UNSET)

        permission = d.pop("permission", UNSET)

        subject_object_type = d.pop("subjectObjectType", UNSET)

        optional_subject_relation = d.pop("optionalSubjectRelation", UNSET)

        _optional_start_cursor = d.pop("optionalStartCursor", UNSET)
        optional_start_cursor: Union[Unset, V1ZedToken]
        if isinstance(_optional_start_cursor, Unset):
            optional_start_cursor = UNSET
        else:
            optional_start_cursor = V1ZedToken.from_dict(_optional_start_cursor)

        v1_alpha_1_watch_resources_request = cls(
            resource_object_type=resource_object_type,
            permission=permission,
            subject_object_type=subject_object_type,
            optional_subject_relation=optional_subject_relation,
            optional_start_cursor=optional_start_cursor,
        )

        v1_alpha_1_watch_resources_request.additional_properties = d
        return v1_alpha_1_watch_resources_request

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
