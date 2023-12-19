from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V1BulkImportRelationshipsResponse")


@_attrs_define
class V1BulkImportRelationshipsResponse:
    """BulkImportRelationshipsResponse is returned on successful completion of the
    bulk load stream, and contains the total number of relationships loaded.

        Attributes:
            num_loaded (Union[Unset, str]):
    """

    num_loaded: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        num_loaded = self.num_loaded

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if num_loaded is not UNSET:
            field_dict["numLoaded"] = num_loaded

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        num_loaded = d.pop("numLoaded", UNSET)

        v1_bulk_import_relationships_response = cls(
            num_loaded=num_loaded,
        )

        v1_bulk_import_relationships_response.additional_properties = d
        return v1_bulk_import_relationships_response

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
