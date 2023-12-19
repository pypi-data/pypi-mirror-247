from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_zed_token import V1ZedToken


T = TypeVar("T", bound="Apiv1ReadSchemaResponse")


@_attrs_define
class Apiv1ReadSchemaResponse:
    """ReadSchemaResponse is the resulting data after having read the Object
    Definitions from a Schema.

        Attributes:
            schema_text (Union[Unset, str]):
            read_at (Union[Unset, V1ZedToken]): ZedToken is used to provide causality metadata between Write and Check
                requests.

                See the authzed.api.v1.Consistency message for more information.
    """

    schema_text: Union[Unset, str] = UNSET
    read_at: Union[Unset, "V1ZedToken"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        schema_text = self.schema_text
        read_at: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.read_at, Unset):
            read_at = self.read_at.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if schema_text is not UNSET:
            field_dict["schemaText"] = schema_text
        if read_at is not UNSET:
            field_dict["readAt"] = read_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_zed_token import V1ZedToken

        d = src_dict.copy()
        schema_text = d.pop("schemaText", UNSET)

        _read_at = d.pop("readAt", UNSET)
        read_at: Union[Unset, V1ZedToken]
        if isinstance(_read_at, Unset):
            read_at = UNSET
        else:
            read_at = V1ZedToken.from_dict(_read_at)

        apiv_1_read_schema_response = cls(
            schema_text=schema_text,
            read_at=read_at,
        )

        apiv_1_read_schema_response.additional_properties = d
        return apiv_1_read_schema_response

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
