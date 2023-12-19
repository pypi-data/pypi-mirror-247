from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_contextualized_caveat_context_consists_of_any_named_values_that_are_defined_at_write_time_for_the_caveat_expression import (
        V1ContextualizedCaveatContextConsistsOfAnyNamedValuesThatAreDefinedAtWriteTimeForTheCaveatExpression,
    )


T = TypeVar("T", bound="V1ContextualizedCaveat")


@_attrs_define
class V1ContextualizedCaveat:
    """ContextualizedCaveat represents a reference to a caveat to be used by caveated relationships.
    The context consists of key-value pairs that will be injected at evaluation time.
    The keys must match the arguments defined on the caveat in the schema.

        Attributes:
            caveat_name (Union[Unset, str]):
            context (Union[Unset,
                V1ContextualizedCaveatContextConsistsOfAnyNamedValuesThatAreDefinedAtWriteTimeForTheCaveatExpression]):
    """

    caveat_name: Union[Unset, str] = UNSET
    context: Union[
        Unset, "V1ContextualizedCaveatContextConsistsOfAnyNamedValuesThatAreDefinedAtWriteTimeForTheCaveatExpression"
    ] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        caveat_name = self.caveat_name
        context: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if caveat_name is not UNSET:
            field_dict["caveatName"] = caveat_name
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_contextualized_caveat_context_consists_of_any_named_values_that_are_defined_at_write_time_for_the_caveat_expression import (
            V1ContextualizedCaveatContextConsistsOfAnyNamedValuesThatAreDefinedAtWriteTimeForTheCaveatExpression,
        )

        d = src_dict.copy()
        caveat_name = d.pop("caveatName", UNSET)

        _context = d.pop("context", UNSET)
        context: Union[
            Unset, V1ContextualizedCaveatContextConsistsOfAnyNamedValuesThatAreDefinedAtWriteTimeForTheCaveatExpression
        ]
        if isinstance(_context, Unset):
            context = UNSET
        else:
            context = V1ContextualizedCaveatContextConsistsOfAnyNamedValuesThatAreDefinedAtWriteTimeForTheCaveatExpression.from_dict(
                _context
            )

        v1_contextualized_caveat = cls(
            caveat_name=caveat_name,
            context=context,
        )

        v1_contextualized_caveat.additional_properties = d
        return v1_contextualized_caveat

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
