from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_consistency import V1Consistency
    from ..models.v1_cursor import V1Cursor
    from ..models.v1_relationship_filter import V1RelationshipFilter


T = TypeVar("T", bound="V1ReadRelationshipsRequest")


@_attrs_define
class V1ReadRelationshipsRequest:
    """ReadRelationshipsRequest specifies one or more filters used to read matching
    relationships within the system.

        Attributes:
            consistency (Union[Unset, V1Consistency]): Consistency will define how a request is handled by the backend.
                By defining a consistency requirement, and a token at which those
                requirements should be applied, where applicable.
            relationship_filter (Union[Unset, V1RelationshipFilter]): RelationshipFilter is a collection of filters which
                when applied to a
                relationship will return relationships that have exactly matching fields.

                resource_type is required. All other fields are optional and if left
                unspecified will not filter relationships.
            optional_limit (Union[Unset, int]): optional_limit, if non-zero, specifies the limit on the number of
                relationships to return
                before the stream is closed on the server side. By default, the stream will continue
                resolving relationships until exhausted or the stream is closed due to the client or a
                network issue.
            optional_cursor (Union[Unset, V1Cursor]): Cursor is used to provide resumption of listing between calls to APIs
                such as LookupResources.
    """

    consistency: Union[Unset, "V1Consistency"] = UNSET
    relationship_filter: Union[Unset, "V1RelationshipFilter"] = UNSET
    optional_limit: Union[Unset, int] = UNSET
    optional_cursor: Union[Unset, "V1Cursor"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        consistency: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.consistency, Unset):
            consistency = self.consistency.to_dict()

        relationship_filter: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.relationship_filter, Unset):
            relationship_filter = self.relationship_filter.to_dict()

        optional_limit = self.optional_limit
        optional_cursor: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.optional_cursor, Unset):
            optional_cursor = self.optional_cursor.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if consistency is not UNSET:
            field_dict["consistency"] = consistency
        if relationship_filter is not UNSET:
            field_dict["relationshipFilter"] = relationship_filter
        if optional_limit is not UNSET:
            field_dict["optionalLimit"] = optional_limit
        if optional_cursor is not UNSET:
            field_dict["optionalCursor"] = optional_cursor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_consistency import V1Consistency
        from ..models.v1_cursor import V1Cursor
        from ..models.v1_relationship_filter import V1RelationshipFilter

        d = src_dict.copy()
        _consistency = d.pop("consistency", UNSET)
        consistency: Union[Unset, V1Consistency]
        if isinstance(_consistency, Unset):
            consistency = UNSET
        else:
            consistency = V1Consistency.from_dict(_consistency)

        _relationship_filter = d.pop("relationshipFilter", UNSET)
        relationship_filter: Union[Unset, V1RelationshipFilter]
        if isinstance(_relationship_filter, Unset):
            relationship_filter = UNSET
        else:
            relationship_filter = V1RelationshipFilter.from_dict(_relationship_filter)

        optional_limit = d.pop("optionalLimit", UNSET)

        _optional_cursor = d.pop("optionalCursor", UNSET)
        optional_cursor: Union[Unset, V1Cursor]
        if isinstance(_optional_cursor, Unset):
            optional_cursor = UNSET
        else:
            optional_cursor = V1Cursor.from_dict(_optional_cursor)

        v1_read_relationships_request = cls(
            consistency=consistency,
            relationship_filter=relationship_filter,
            optional_limit=optional_limit,
            optional_cursor=optional_cursor,
        )

        v1_read_relationships_request.additional_properties = d
        return v1_read_relationships_request

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
