from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_relationship import V1Relationship


T = TypeVar("T", bound="V1BulkImportRelationshipsRequest")


@_attrs_define
class V1BulkImportRelationshipsRequest:
    """BulkImportRelationshipsRequest represents one batch of the streaming
    BulkImportRelationships API. The maximum size is only limited by the backing
    datastore, and optimal size should be determined by the calling client
    experimentally.

        Attributes:
            relationships (Union[Unset, List['V1Relationship']]):
    """

    relationships: Union[Unset, List["V1Relationship"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        relationships: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.relationships, Unset):
            relationships = []
            for relationships_item_data in self.relationships:
                relationships_item = relationships_item_data.to_dict()

                relationships.append(relationships_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if relationships is not UNSET:
            field_dict["relationships"] = relationships

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_relationship import V1Relationship

        d = src_dict.copy()
        relationships = []
        _relationships = d.pop("relationships", UNSET)
        for relationships_item_data in _relationships or []:
            relationships_item = V1Relationship.from_dict(relationships_item_data)

            relationships.append(relationships_item)

        v1_bulk_import_relationships_request = cls(
            relationships=relationships,
        )

        v1_bulk_import_relationships_request.additional_properties = d
        return v1_bulk_import_relationships_request

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
