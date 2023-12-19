from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.lookup_share_response_lookup_status import LookupShareResponseLookupStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="V0LookupShareResponse")


@_attrs_define
class V0LookupShareResponse:
    """
    Attributes:
        status (Union[Unset, LookupShareResponseLookupStatus]):  Default:
            LookupShareResponseLookupStatus.UNKNOWN_REFERENCE.
        schema (Union[Unset, str]):
        relationships_yaml (Union[Unset, str]):
        validation_yaml (Union[Unset, str]):
        assertions_yaml (Union[Unset, str]):
    """

    status: Union[Unset, LookupShareResponseLookupStatus] = LookupShareResponseLookupStatus.UNKNOWN_REFERENCE
    schema: Union[Unset, str] = UNSET
    relationships_yaml: Union[Unset, str] = UNSET
    validation_yaml: Union[Unset, str] = UNSET
    assertions_yaml: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        schema = self.schema
        relationships_yaml = self.relationships_yaml
        validation_yaml = self.validation_yaml
        assertions_yaml = self.assertions_yaml

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if schema is not UNSET:
            field_dict["schema"] = schema
        if relationships_yaml is not UNSET:
            field_dict["relationshipsYaml"] = relationships_yaml
        if validation_yaml is not UNSET:
            field_dict["validationYaml"] = validation_yaml
        if assertions_yaml is not UNSET:
            field_dict["assertionsYaml"] = assertions_yaml

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _status = d.pop("status", UNSET)
        status: Union[Unset, LookupShareResponseLookupStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = LookupShareResponseLookupStatus(_status)

        schema = d.pop("schema", UNSET)

        relationships_yaml = d.pop("relationshipsYaml", UNSET)

        validation_yaml = d.pop("validationYaml", UNSET)

        assertions_yaml = d.pop("assertionsYaml", UNSET)

        v0_lookup_share_response = cls(
            status=status,
            schema=schema,
            relationships_yaml=relationships_yaml,
            validation_yaml=validation_yaml,
            assertions_yaml=assertions_yaml,
        )

        v0_lookup_share_response.additional_properties = d
        return v0_lookup_share_response

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
