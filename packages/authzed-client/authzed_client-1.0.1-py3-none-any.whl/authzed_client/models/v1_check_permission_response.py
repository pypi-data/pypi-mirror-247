from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v1_check_permission_response_permissionship import V1CheckPermissionResponsePermissionship
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_partial_caveat_info import V1PartialCaveatInfo
    from ..models.v1_zed_token import V1ZedToken


T = TypeVar("T", bound="V1CheckPermissionResponse")


@_attrs_define
class V1CheckPermissionResponse:
    """
    Attributes:
        checked_at (Union[Unset, V1ZedToken]): ZedToken is used to provide causality metadata between Write and Check
            requests.

            See the authzed.api.v1.Consistency message for more information.
        permissionship (Union[Unset, V1CheckPermissionResponsePermissionship]):  Default:
            V1CheckPermissionResponsePermissionship.PERMISSIONSHIP_UNSPECIFIED.
        partial_caveat_info (Union[Unset, V1PartialCaveatInfo]): PartialCaveatInfo carries information necessary for the
            client to take action
            in the event a response contains a partially evaluated caveat
    """

    checked_at: Union[Unset, "V1ZedToken"] = UNSET
    permissionship: Union[
        Unset, V1CheckPermissionResponsePermissionship
    ] = V1CheckPermissionResponsePermissionship.PERMISSIONSHIP_UNSPECIFIED
    partial_caveat_info: Union[Unset, "V1PartialCaveatInfo"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        checked_at: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.checked_at, Unset):
            checked_at = self.checked_at.to_dict()

        permissionship: Union[Unset, str] = UNSET
        if not isinstance(self.permissionship, Unset):
            permissionship = self.permissionship.value

        partial_caveat_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.partial_caveat_info, Unset):
            partial_caveat_info = self.partial_caveat_info.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if checked_at is not UNSET:
            field_dict["checkedAt"] = checked_at
        if permissionship is not UNSET:
            field_dict["permissionship"] = permissionship
        if partial_caveat_info is not UNSET:
            field_dict["partialCaveatInfo"] = partial_caveat_info

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_partial_caveat_info import V1PartialCaveatInfo
        from ..models.v1_zed_token import V1ZedToken

        d = src_dict.copy()
        _checked_at = d.pop("checkedAt", UNSET)
        checked_at: Union[Unset, V1ZedToken]
        if isinstance(_checked_at, Unset):
            checked_at = UNSET
        else:
            checked_at = V1ZedToken.from_dict(_checked_at)

        _permissionship = d.pop("permissionship", UNSET)
        permissionship: Union[Unset, V1CheckPermissionResponsePermissionship]
        if isinstance(_permissionship, Unset):
            permissionship = UNSET
        else:
            permissionship = V1CheckPermissionResponsePermissionship(_permissionship)

        _partial_caveat_info = d.pop("partialCaveatInfo", UNSET)
        partial_caveat_info: Union[Unset, V1PartialCaveatInfo]
        if isinstance(_partial_caveat_info, Unset):
            partial_caveat_info = UNSET
        else:
            partial_caveat_info = V1PartialCaveatInfo.from_dict(_partial_caveat_info)

        v1_check_permission_response = cls(
            checked_at=checked_at,
            permissionship=permissionship,
            partial_caveat_info=partial_caveat_info,
        )

        v1_check_permission_response.additional_properties = d
        return v1_check_permission_response

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
