from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0_object_and_relation import V0ObjectAndRelation
    from ..models.v0_user import V0User


T = TypeVar("T", bound="V0RelationTuple")


@_attrs_define
class V0RelationTuple:
    """
    Attributes:
        object_and_relation (Union[Unset, V0ObjectAndRelation]):
        user (Union[Unset, V0User]):
    """

    object_and_relation: Union[Unset, "V0ObjectAndRelation"] = UNSET
    user: Union[Unset, "V0User"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        object_and_relation: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.object_and_relation, Unset):
            object_and_relation = self.object_and_relation.to_dict()

        user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if object_and_relation is not UNSET:
            field_dict["objectAndRelation"] = object_and_relation
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v0_object_and_relation import V0ObjectAndRelation
        from ..models.v0_user import V0User

        d = src_dict.copy()
        _object_and_relation = d.pop("objectAndRelation", UNSET)
        object_and_relation: Union[Unset, V0ObjectAndRelation]
        if isinstance(_object_and_relation, Unset):
            object_and_relation = UNSET
        else:
            object_and_relation = V0ObjectAndRelation.from_dict(_object_and_relation)

        _user = d.pop("user", UNSET)
        user: Union[Unset, V0User]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = V0User.from_dict(_user)

        v0_relation_tuple = cls(
            object_and_relation=object_and_relation,
            user=user,
        )

        v0_relation_tuple.additional_properties = d
        return v0_relation_tuple

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
