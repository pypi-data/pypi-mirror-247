from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0_developer_error import V0DeveloperError


T = TypeVar("T", bound="V0FormatSchemaResponse")


@_attrs_define
class V0FormatSchemaResponse:
    """
    Attributes:
        error (Union[Unset, V0DeveloperError]):
        formatted_schema (Union[Unset, str]):
    """

    error: Union[Unset, "V0DeveloperError"] = UNSET
    formatted_schema: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        error: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        formatted_schema = self.formatted_schema

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error is not UNSET:
            field_dict["error"] = error
        if formatted_schema is not UNSET:
            field_dict["formattedSchema"] = formatted_schema

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

        formatted_schema = d.pop("formattedSchema", UNSET)

        v0_format_schema_response = cls(
            error=error,
            formatted_schema=formatted_schema,
        )

        v0_format_schema_response.additional_properties = d
        return v0_format_schema_response

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
