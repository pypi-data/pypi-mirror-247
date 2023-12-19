from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_zed_token import V1ZedToken


T = TypeVar("T", bound="V1WatchRequest")


@_attrs_define
class V1WatchRequest:
    """WatchRequest specifies the object definitions for which we want to start
    watching mutations, and an optional start snapshot for when to start
    watching.

        Attributes:
            optional_object_types (Union[Unset, List[str]]):
            optional_start_cursor (Union[Unset, V1ZedToken]): ZedToken is used to provide causality metadata between Write
                and Check
                requests.

                See the authzed.api.v1.Consistency message for more information.
    """

    optional_object_types: Union[Unset, List[str]] = UNSET
    optional_start_cursor: Union[Unset, "V1ZedToken"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        optional_object_types: Union[Unset, List[str]] = UNSET
        if not isinstance(self.optional_object_types, Unset):
            optional_object_types = self.optional_object_types

        optional_start_cursor: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.optional_start_cursor, Unset):
            optional_start_cursor = self.optional_start_cursor.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if optional_object_types is not UNSET:
            field_dict["optionalObjectTypes"] = optional_object_types
        if optional_start_cursor is not UNSET:
            field_dict["optionalStartCursor"] = optional_start_cursor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_zed_token import V1ZedToken

        d = src_dict.copy()
        optional_object_types = cast(List[str], d.pop("optionalObjectTypes", UNSET))

        _optional_start_cursor = d.pop("optionalStartCursor", UNSET)
        optional_start_cursor: Union[Unset, V1ZedToken]
        if isinstance(_optional_start_cursor, Unset):
            optional_start_cursor = UNSET
        else:
            optional_start_cursor = V1ZedToken.from_dict(_optional_start_cursor)

        v1_watch_request = cls(
            optional_object_types=optional_object_types,
            optional_start_cursor=optional_start_cursor,
        )

        v1_watch_request.additional_properties = d
        return v1_watch_request

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
