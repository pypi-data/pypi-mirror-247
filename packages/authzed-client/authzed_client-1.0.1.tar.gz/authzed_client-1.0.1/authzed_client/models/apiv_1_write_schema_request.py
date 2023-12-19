from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Apiv1WriteSchemaRequest")


@_attrs_define
class Apiv1WriteSchemaRequest:
    """WriteSchemaRequest is the required data used to "upsert" the Schema of a
    Permissions System.

        Attributes:
            schema (Union[Unset, str]): The Schema containing one or more Object Definitions that will be written
                to the Permissions System.

                4MiB
    """

    schema: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        schema = self.schema

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        schema = d.pop("schema", UNSET)

        apiv_1_write_schema_request = cls(
            schema=schema,
        )

        apiv_1_write_schema_request.additional_properties = d
        return apiv_1_write_schema_request

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
