from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Apiv1Alpha1ReadSchemaResponse")


@_attrs_define
class Apiv1Alpha1ReadSchemaResponse:
    """ReadSchemaResponse is the resulting data after having read the Object
    Definitions from a Schema.

        Attributes:
            object_definitions (Union[Unset, List[str]]): The Object Definitions that were requested.
            computed_definitions_revision (Union[Unset, str]): The computed revision of the returned object definitions.
    """

    object_definitions: Union[Unset, List[str]] = UNSET
    computed_definitions_revision: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        object_definitions: Union[Unset, List[str]] = UNSET
        if not isinstance(self.object_definitions, Unset):
            object_definitions = self.object_definitions

        computed_definitions_revision = self.computed_definitions_revision

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if object_definitions is not UNSET:
            field_dict["objectDefinitions"] = object_definitions
        if computed_definitions_revision is not UNSET:
            field_dict["computedDefinitionsRevision"] = computed_definitions_revision

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_definitions = cast(List[str], d.pop("objectDefinitions", UNSET))

        computed_definitions_revision = d.pop("computedDefinitionsRevision", UNSET)

        apiv_1_alpha_1_read_schema_response = cls(
            object_definitions=object_definitions,
            computed_definitions_revision=computed_definitions_revision,
        )

        apiv_1_alpha_1_read_schema_response.additional_properties = d
        return apiv_1_alpha_1_read_schema_response

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
