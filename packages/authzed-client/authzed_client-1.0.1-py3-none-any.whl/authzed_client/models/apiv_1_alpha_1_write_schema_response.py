from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Apiv1Alpha1WriteSchemaResponse")


@_attrs_define
class Apiv1Alpha1WriteSchemaResponse:
    """WriteSchemaResponse is the resulting data after having written a Schema to
    a Permissions System.

        Attributes:
            object_definitions_names (Union[Unset, List[str]]): The names of the Object Definitions that were written.
            computed_definitions_revision (Union[Unset, str]): The computed revision of the written object definitions.
    """

    object_definitions_names: Union[Unset, List[str]] = UNSET
    computed_definitions_revision: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        object_definitions_names: Union[Unset, List[str]] = UNSET
        if not isinstance(self.object_definitions_names, Unset):
            object_definitions_names = self.object_definitions_names

        computed_definitions_revision = self.computed_definitions_revision

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if object_definitions_names is not UNSET:
            field_dict["objectDefinitionsNames"] = object_definitions_names
        if computed_definitions_revision is not UNSET:
            field_dict["computedDefinitionsRevision"] = computed_definitions_revision

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_definitions_names = cast(List[str], d.pop("objectDefinitionsNames", UNSET))

        computed_definitions_revision = d.pop("computedDefinitionsRevision", UNSET)

        apiv_1_alpha_1_write_schema_response = cls(
            object_definitions_names=object_definitions_names,
            computed_definitions_revision=computed_definitions_revision,
        )

        apiv_1_alpha_1_write_schema_response.additional_properties = d
        return apiv_1_alpha_1_write_schema_response

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
