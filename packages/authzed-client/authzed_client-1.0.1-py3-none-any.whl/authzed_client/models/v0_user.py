from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0_object_and_relation import V0ObjectAndRelation


T = TypeVar("T", bound="V0User")


@_attrs_define
class V0User:
    """
    Attributes:
        userset (Union[Unset, V0ObjectAndRelation]):
    """

    userset: Union[Unset, "V0ObjectAndRelation"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        userset: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.userset, Unset):
            userset = self.userset.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if userset is not UNSET:
            field_dict["userset"] = userset

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v0_object_and_relation import V0ObjectAndRelation

        d = src_dict.copy()
        _userset = d.pop("userset", UNSET)
        userset: Union[Unset, V0ObjectAndRelation]
        if isinstance(_userset, Unset):
            userset = UNSET
        else:
            userset = V0ObjectAndRelation.from_dict(_userset)

        v0_user = cls(
            userset=userset,
        )

        v0_user.additional_properties = d
        return v0_user

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
