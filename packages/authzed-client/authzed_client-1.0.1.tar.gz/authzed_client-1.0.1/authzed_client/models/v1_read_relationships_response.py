from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_cursor import V1Cursor
    from ..models.v1_relationship import V1Relationship
    from ..models.v1_zed_token import V1ZedToken


T = TypeVar("T", bound="V1ReadRelationshipsResponse")


@_attrs_define
class V1ReadRelationshipsResponse:
    """ReadRelationshipsResponse contains a Relationship found that matches the
    specified relationship filter(s). A instance of this response message will
    be streamed to the client for each relationship found.

        Attributes:
            read_at (Union[Unset, V1ZedToken]): ZedToken is used to provide causality metadata between Write and Check
                requests.

                See the authzed.api.v1.Consistency message for more information.
            relationship (Union[Unset, V1Relationship]): Relationship specifies how a resource relates to a subject.
                Relationships
                form the data for the graph over which all permissions questions are
                answered.
            after_result_cursor (Union[Unset, V1Cursor]): Cursor is used to provide resumption of listing between calls to
                APIs
                such as LookupResources.
    """

    read_at: Union[Unset, "V1ZedToken"] = UNSET
    relationship: Union[Unset, "V1Relationship"] = UNSET
    after_result_cursor: Union[Unset, "V1Cursor"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        read_at: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.read_at, Unset):
            read_at = self.read_at.to_dict()

        relationship: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.relationship, Unset):
            relationship = self.relationship.to_dict()

        after_result_cursor: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.after_result_cursor, Unset):
            after_result_cursor = self.after_result_cursor.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if read_at is not UNSET:
            field_dict["readAt"] = read_at
        if relationship is not UNSET:
            field_dict["relationship"] = relationship
        if after_result_cursor is not UNSET:
            field_dict["afterResultCursor"] = after_result_cursor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_cursor import V1Cursor
        from ..models.v1_relationship import V1Relationship
        from ..models.v1_zed_token import V1ZedToken

        d = src_dict.copy()
        _read_at = d.pop("readAt", UNSET)
        read_at: Union[Unset, V1ZedToken]
        if isinstance(_read_at, Unset):
            read_at = UNSET
        else:
            read_at = V1ZedToken.from_dict(_read_at)

        _relationship = d.pop("relationship", UNSET)
        relationship: Union[Unset, V1Relationship]
        if isinstance(_relationship, Unset):
            relationship = UNSET
        else:
            relationship = V1Relationship.from_dict(_relationship)

        _after_result_cursor = d.pop("afterResultCursor", UNSET)
        after_result_cursor: Union[Unset, V1Cursor]
        if isinstance(_after_result_cursor, Unset):
            after_result_cursor = UNSET
        else:
            after_result_cursor = V1Cursor.from_dict(_after_result_cursor)

        v1_read_relationships_response = cls(
            read_at=read_at,
            relationship=relationship,
            after_result_cursor=after_result_cursor,
        )

        v1_read_relationships_response.additional_properties = d
        return v1_read_relationships_response

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
