from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_consistency import V1Consistency
    from ..models.v1_cursor import V1Cursor


T = TypeVar("T", bound="V1BulkExportRelationshipsRequest")


@_attrs_define
class V1BulkExportRelationshipsRequest:
    """BulkExportRelationshipsRequest represents a resumable request for
    all relationships from the server.

        Attributes:
            consistency (Union[Unset, V1Consistency]): Consistency will define how a request is handled by the backend.
                By defining a consistency requirement, and a token at which those
                requirements should be applied, where applicable.
            optional_limit (Union[Unset, int]): optional_limit, if non-zero, specifies the limit on the number of
                relationships the server can return in one page. By default, the server
                will pick a page size, and the server is free to choose a smaller size
                at will.
            optional_cursor (Union[Unset, V1Cursor]): Cursor is used to provide resumption of listing between calls to APIs
                such as LookupResources.
    """

    consistency: Union[Unset, "V1Consistency"] = UNSET
    optional_limit: Union[Unset, int] = UNSET
    optional_cursor: Union[Unset, "V1Cursor"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        consistency: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.consistency, Unset):
            consistency = self.consistency.to_dict()

        optional_limit = self.optional_limit
        optional_cursor: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.optional_cursor, Unset):
            optional_cursor = self.optional_cursor.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if consistency is not UNSET:
            field_dict["consistency"] = consistency
        if optional_limit is not UNSET:
            field_dict["optionalLimit"] = optional_limit
        if optional_cursor is not UNSET:
            field_dict["optionalCursor"] = optional_cursor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_consistency import V1Consistency
        from ..models.v1_cursor import V1Cursor

        d = src_dict.copy()
        _consistency = d.pop("consistency", UNSET)
        consistency: Union[Unset, V1Consistency]
        if isinstance(_consistency, Unset):
            consistency = UNSET
        else:
            consistency = V1Consistency.from_dict(_consistency)

        optional_limit = d.pop("optionalLimit", UNSET)

        _optional_cursor = d.pop("optionalCursor", UNSET)
        optional_cursor: Union[Unset, V1Cursor]
        if isinstance(_optional_cursor, Unset):
            optional_cursor = UNSET
        else:
            optional_cursor = V1Cursor.from_dict(_optional_cursor)

        v1_bulk_export_relationships_request = cls(
            consistency=consistency,
            optional_limit=optional_limit,
            optional_cursor=optional_cursor,
        )

        v1_bulk_export_relationships_request.additional_properties = d
        return v1_bulk_export_relationships_request

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
