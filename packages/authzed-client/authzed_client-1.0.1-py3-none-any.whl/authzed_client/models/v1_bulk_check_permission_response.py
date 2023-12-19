from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_bulk_check_permission_pair import V1BulkCheckPermissionPair
    from ..models.v1_zed_token import V1ZedToken


T = TypeVar("T", bound="V1BulkCheckPermissionResponse")


@_attrs_define
class V1BulkCheckPermissionResponse:
    """
    Attributes:
        checked_at (Union[Unset, V1ZedToken]): ZedToken is used to provide causality metadata between Write and Check
            requests.

            See the authzed.api.v1.Consistency message for more information.
        pairs (Union[Unset, List['V1BulkCheckPermissionPair']]):
    """

    checked_at: Union[Unset, "V1ZedToken"] = UNSET
    pairs: Union[Unset, List["V1BulkCheckPermissionPair"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        checked_at: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.checked_at, Unset):
            checked_at = self.checked_at.to_dict()

        pairs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.pairs, Unset):
            pairs = []
            for pairs_item_data in self.pairs:
                pairs_item = pairs_item_data.to_dict()

                pairs.append(pairs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if checked_at is not UNSET:
            field_dict["checkedAt"] = checked_at
        if pairs is not UNSET:
            field_dict["pairs"] = pairs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_bulk_check_permission_pair import V1BulkCheckPermissionPair
        from ..models.v1_zed_token import V1ZedToken

        d = src_dict.copy()
        _checked_at = d.pop("checkedAt", UNSET)
        checked_at: Union[Unset, V1ZedToken]
        if isinstance(_checked_at, Unset):
            checked_at = UNSET
        else:
            checked_at = V1ZedToken.from_dict(_checked_at)

        pairs = []
        _pairs = d.pop("pairs", UNSET)
        for pairs_item_data in _pairs or []:
            pairs_item = V1BulkCheckPermissionPair.from_dict(pairs_item_data)

            pairs.append(pairs_item)

        v1_bulk_check_permission_response = cls(
            checked_at=checked_at,
            pairs=pairs,
        )

        v1_bulk_check_permission_response.additional_properties = d
        return v1_bulk_check_permission_response

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
