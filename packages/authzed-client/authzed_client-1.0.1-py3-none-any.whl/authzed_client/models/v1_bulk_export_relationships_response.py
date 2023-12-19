from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_cursor import V1Cursor
    from ..models.v1_relationship import V1Relationship


T = TypeVar("T", bound="V1BulkExportRelationshipsResponse")


@_attrs_define
class V1BulkExportRelationshipsResponse:
    """BulkExportRelationshipsResponse is one page in a stream of relationship
    groups that meet the criteria specified by the originating request. The
    server will continue to stream back relationship groups as quickly as it can
    until all relationships have been transmitted back.

        Attributes:
            after_result_cursor (Union[Unset, V1Cursor]): Cursor is used to provide resumption of listing between calls to
                APIs
                such as LookupResources.
            relationships (Union[Unset, List['V1Relationship']]):
    """

    after_result_cursor: Union[Unset, "V1Cursor"] = UNSET
    relationships: Union[Unset, List["V1Relationship"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        after_result_cursor: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.after_result_cursor, Unset):
            after_result_cursor = self.after_result_cursor.to_dict()

        relationships: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.relationships, Unset):
            relationships = []
            for relationships_item_data in self.relationships:
                relationships_item = relationships_item_data.to_dict()

                relationships.append(relationships_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if after_result_cursor is not UNSET:
            field_dict["afterResultCursor"] = after_result_cursor
        if relationships is not UNSET:
            field_dict["relationships"] = relationships

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_cursor import V1Cursor
        from ..models.v1_relationship import V1Relationship

        d = src_dict.copy()
        _after_result_cursor = d.pop("afterResultCursor", UNSET)
        after_result_cursor: Union[Unset, V1Cursor]
        if isinstance(_after_result_cursor, Unset):
            after_result_cursor = UNSET
        else:
            after_result_cursor = V1Cursor.from_dict(_after_result_cursor)

        relationships = []
        _relationships = d.pop("relationships", UNSET)
        for relationships_item_data in _relationships or []:
            relationships_item = V1Relationship.from_dict(relationships_item_data)

            relationships.append(relationships_item)

        v1_bulk_export_relationships_response = cls(
            after_result_cursor=after_result_cursor,
            relationships=relationships,
        )

        v1_bulk_export_relationships_response.additional_properties = d
        return v1_bulk_export_relationships_response

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
