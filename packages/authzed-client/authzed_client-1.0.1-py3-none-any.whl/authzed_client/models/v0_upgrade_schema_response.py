from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0_developer_error import V0DeveloperError


T = TypeVar("T", bound="V0UpgradeSchemaResponse")


@_attrs_define
class V0UpgradeSchemaResponse:
    """
    Attributes:
        error (Union[Unset, V0DeveloperError]):
        upgraded_schema (Union[Unset, str]):
    """

    error: Union[Unset, "V0DeveloperError"] = UNSET
    upgraded_schema: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        error: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        upgraded_schema = self.upgraded_schema

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error is not UNSET:
            field_dict["error"] = error
        if upgraded_schema is not UNSET:
            field_dict["upgradedSchema"] = upgraded_schema

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v0_developer_error import V0DeveloperError

        d = src_dict.copy()
        _error = d.pop("error", UNSET)
        error: Union[Unset, V0DeveloperError]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = V0DeveloperError.from_dict(_error)

        upgraded_schema = d.pop("upgradedSchema", UNSET)

        v0_upgrade_schema_response = cls(
            error=error,
            upgraded_schema=upgraded_schema,
        )

        v0_upgrade_schema_response.additional_properties = d
        return v0_upgrade_schema_response

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
