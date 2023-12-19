from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0_relation_tuple import V0RelationTuple


T = TypeVar("T", bound="V0RequestContext")


@_attrs_define
class V0RequestContext:
    """
    Attributes:
        schema (Union[Unset, str]):
        relationships (Union[Unset, List['V0RelationTuple']]):
    """

    schema: Union[Unset, str] = UNSET
    relationships: Union[Unset, List["V0RelationTuple"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        schema = self.schema
        relationships: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.relationships, Unset):
            relationships = []
            for relationships_item_data in self.relationships:
                relationships_item = relationships_item_data.to_dict()

                relationships.append(relationships_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if schema is not UNSET:
            field_dict["schema"] = schema
        if relationships is not UNSET:
            field_dict["relationships"] = relationships

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v0_relation_tuple import V0RelationTuple

        d = src_dict.copy()
        schema = d.pop("schema", UNSET)

        relationships = []
        _relationships = d.pop("relationships", UNSET)
        for relationships_item_data in _relationships or []:
            relationships_item = V0RelationTuple.from_dict(relationships_item_data)

            relationships.append(relationships_item)

        v0_request_context = cls(
            schema=schema,
            relationships=relationships,
        )

        v0_request_context.additional_properties = d
        return v0_request_context

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
