from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_precondition import V1Precondition
    from ..models.v1_relationship_update import V1RelationshipUpdate


T = TypeVar("T", bound="V1WriteRelationshipsRequest")


@_attrs_define
class V1WriteRelationshipsRequest:
    """WriteRelationshipsRequest contains a list of Relationship mutations that
    should be applied to the service. If the optional_preconditions parameter
    is included, all of the specified preconditions must also be satisfied before
    the write will be committed.

        Attributes:
            updates (Union[Unset, List['V1RelationshipUpdate']]):
            optional_preconditions (Union[Unset, List['V1Precondition']]):
    """

    updates: Union[Unset, List["V1RelationshipUpdate"]] = UNSET
    optional_preconditions: Union[Unset, List["V1Precondition"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        updates: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.updates, Unset):
            updates = []
            for updates_item_data in self.updates:
                updates_item = updates_item_data.to_dict()

                updates.append(updates_item)

        optional_preconditions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.optional_preconditions, Unset):
            optional_preconditions = []
            for optional_preconditions_item_data in self.optional_preconditions:
                optional_preconditions_item = optional_preconditions_item_data.to_dict()

                optional_preconditions.append(optional_preconditions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if updates is not UNSET:
            field_dict["updates"] = updates
        if optional_preconditions is not UNSET:
            field_dict["optionalPreconditions"] = optional_preconditions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_precondition import V1Precondition
        from ..models.v1_relationship_update import V1RelationshipUpdate

        d = src_dict.copy()
        updates = []
        _updates = d.pop("updates", UNSET)
        for updates_item_data in _updates or []:
            updates_item = V1RelationshipUpdate.from_dict(updates_item_data)

            updates.append(updates_item)

        optional_preconditions = []
        _optional_preconditions = d.pop("optionalPreconditions", UNSET)
        for optional_preconditions_item_data in _optional_preconditions or []:
            optional_preconditions_item = V1Precondition.from_dict(optional_preconditions_item_data)

            optional_preconditions.append(optional_preconditions_item)

        v1_write_relationships_request = cls(
            updates=updates,
            optional_preconditions=optional_preconditions,
        )

        v1_write_relationships_request.additional_properties = d
        return v1_write_relationships_request

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
