from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_alpha_1_permission_update import V1Alpha1PermissionUpdate
    from ..models.v1_zed_token import V1ZedToken


T = TypeVar("T", bound="V1Alpha1WatchResourcesResponse")


@_attrs_define
class V1Alpha1WatchResourcesResponse:
    """WatchResourcesResponse enumerates the list of permission updates that have
    occurred as a result of one or more relationship updates.

        Attributes:
            updates (Union[Unset, List['V1Alpha1PermissionUpdate']]):
            changes_through (Union[Unset, V1ZedToken]): ZedToken is used to provide causality metadata between Write and
                Check
                requests.

                See the authzed.api.v1.Consistency message for more information.
    """

    updates: Union[Unset, List["V1Alpha1PermissionUpdate"]] = UNSET
    changes_through: Union[Unset, "V1ZedToken"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        updates: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.updates, Unset):
            updates = []
            for updates_item_data in self.updates:
                updates_item = updates_item_data.to_dict()

                updates.append(updates_item)

        changes_through: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.changes_through, Unset):
            changes_through = self.changes_through.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if updates is not UNSET:
            field_dict["updates"] = updates
        if changes_through is not UNSET:
            field_dict["changesThrough"] = changes_through

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_alpha_1_permission_update import V1Alpha1PermissionUpdate
        from ..models.v1_zed_token import V1ZedToken

        d = src_dict.copy()
        updates = []
        _updates = d.pop("updates", UNSET)
        for updates_item_data in _updates or []:
            updates_item = V1Alpha1PermissionUpdate.from_dict(updates_item_data)

            updates.append(updates_item)

        _changes_through = d.pop("changesThrough", UNSET)
        changes_through: Union[Unset, V1ZedToken]
        if isinstance(_changes_through, Unset):
            changes_through = UNSET
        else:
            changes_through = V1ZedToken.from_dict(_changes_through)

        v1_alpha_1_watch_resources_response = cls(
            updates=updates,
            changes_through=changes_through,
        )

        v1_alpha_1_watch_resources_response.additional_properties = d
        return v1_alpha_1_watch_resources_response

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
