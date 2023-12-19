from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_precondition import V1Precondition
    from ..models.v1_relationship_filter import V1RelationshipFilter


T = TypeVar("T", bound="V1DeleteRelationshipsRequest")


@_attrs_define
class V1DeleteRelationshipsRequest:
    """DeleteRelationshipsRequest specifies which Relationships should be deleted,
    requesting the delete of *ALL* relationships that match the specified
    filters. If the optional_preconditions parameter is included, all of the
    specified preconditions must also be satisfied before the delete will be
    executed.

        Attributes:
            relationship_filter (Union[Unset, V1RelationshipFilter]): RelationshipFilter is a collection of filters which
                when applied to a
                relationship will return relationships that have exactly matching fields.

                resource_type is required. All other fields are optional and if left
                unspecified will not filter relationships.
            optional_preconditions (Union[Unset, List['V1Precondition']]):
            optional_limit (Union[Unset, int]): optional_limit, if non-zero, specifies the limit on the number of
                relationships to be deleted.
                If there are more matching relationships found to be deleted than the limit specified here,
                the deletion call will fail with an error to prevent partial deletion. If partial deletion
                is needed, specify below that partial deletion is allowed. Partial deletions can be used
                in a loop to delete large amounts of relationships in a *non-transactional* manner.
            optional_allow_partial_deletions (Union[Unset, bool]): optional_allow_partial_deletions, if true and a limit is
                specified, will delete matching found
                relationships up to the count specified in optional_limit, and no more.
    """

    relationship_filter: Union[Unset, "V1RelationshipFilter"] = UNSET
    optional_preconditions: Union[Unset, List["V1Precondition"]] = UNSET
    optional_limit: Union[Unset, int] = UNSET
    optional_allow_partial_deletions: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        relationship_filter: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.relationship_filter, Unset):
            relationship_filter = self.relationship_filter.to_dict()

        optional_preconditions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.optional_preconditions, Unset):
            optional_preconditions = []
            for optional_preconditions_item_data in self.optional_preconditions:
                optional_preconditions_item = optional_preconditions_item_data.to_dict()

                optional_preconditions.append(optional_preconditions_item)

        optional_limit = self.optional_limit
        optional_allow_partial_deletions = self.optional_allow_partial_deletions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if relationship_filter is not UNSET:
            field_dict["relationshipFilter"] = relationship_filter
        if optional_preconditions is not UNSET:
            field_dict["optionalPreconditions"] = optional_preconditions
        if optional_limit is not UNSET:
            field_dict["optionalLimit"] = optional_limit
        if optional_allow_partial_deletions is not UNSET:
            field_dict["optionalAllowPartialDeletions"] = optional_allow_partial_deletions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_precondition import V1Precondition
        from ..models.v1_relationship_filter import V1RelationshipFilter

        d = src_dict.copy()
        _relationship_filter = d.pop("relationshipFilter", UNSET)
        relationship_filter: Union[Unset, V1RelationshipFilter]
        if isinstance(_relationship_filter, Unset):
            relationship_filter = UNSET
        else:
            relationship_filter = V1RelationshipFilter.from_dict(_relationship_filter)

        optional_preconditions = []
        _optional_preconditions = d.pop("optionalPreconditions", UNSET)
        for optional_preconditions_item_data in _optional_preconditions or []:
            optional_preconditions_item = V1Precondition.from_dict(optional_preconditions_item_data)

            optional_preconditions.append(optional_preconditions_item)

        optional_limit = d.pop("optionalLimit", UNSET)

        optional_allow_partial_deletions = d.pop("optionalAllowPartialDeletions", UNSET)

        v1_delete_relationships_request = cls(
            relationship_filter=relationship_filter,
            optional_preconditions=optional_preconditions,
            optional_limit=optional_limit,
            optional_allow_partial_deletions=optional_allow_partial_deletions,
        )

        v1_delete_relationships_request.additional_properties = d
        return v1_delete_relationships_request

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
