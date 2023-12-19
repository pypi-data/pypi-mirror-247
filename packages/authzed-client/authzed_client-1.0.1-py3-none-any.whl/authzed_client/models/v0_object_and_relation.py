from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V0ObjectAndRelation")


@_attrs_define
class V0ObjectAndRelation:
    """
    Attributes:
        namespace (Union[Unset, str]):
        object_id (Union[Unset, str]):
        relation (Union[Unset, str]):
    """

    namespace: Union[Unset, str] = UNSET
    object_id: Union[Unset, str] = UNSET
    relation: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        namespace = self.namespace
        object_id = self.object_id
        relation = self.relation

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if namespace is not UNSET:
            field_dict["namespace"] = namespace
        if object_id is not UNSET:
            field_dict["objectId"] = object_id
        if relation is not UNSET:
            field_dict["relation"] = relation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        namespace = d.pop("namespace", UNSET)

        object_id = d.pop("objectId", UNSET)

        relation = d.pop("relation", UNSET)

        v0_object_and_relation = cls(
            namespace=namespace,
            object_id=object_id,
            relation=relation,
        )

        v0_object_and_relation.additional_properties = d
        return v0_object_and_relation

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
