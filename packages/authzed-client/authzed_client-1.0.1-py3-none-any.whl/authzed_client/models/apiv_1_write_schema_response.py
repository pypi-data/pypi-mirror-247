from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_zed_token import V1ZedToken


T = TypeVar("T", bound="Apiv1WriteSchemaResponse")


@_attrs_define
class Apiv1WriteSchemaResponse:
    """WriteSchemaResponse is the resulting data after having written a Schema to
    a Permissions System.

        Attributes:
            written_at (Union[Unset, V1ZedToken]): ZedToken is used to provide causality metadata between Write and Check
                requests.

                See the authzed.api.v1.Consistency message for more information.
    """

    written_at: Union[Unset, "V1ZedToken"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        written_at: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.written_at, Unset):
            written_at = self.written_at.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if written_at is not UNSET:
            field_dict["writtenAt"] = written_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_zed_token import V1ZedToken

        d = src_dict.copy()
        _written_at = d.pop("writtenAt", UNSET)
        written_at: Union[Unset, V1ZedToken]
        if isinstance(_written_at, Unset):
            written_at = UNSET
        else:
            written_at = V1ZedToken.from_dict(_written_at)

        apiv_1_write_schema_response = cls(
            written_at=written_at,
        )

        apiv_1_write_schema_response.additional_properties = d
        return apiv_1_write_schema_response

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
