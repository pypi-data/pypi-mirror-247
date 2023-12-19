from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v1_precondition_operation import V1PreconditionOperation
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_relationship_filter import V1RelationshipFilter


T = TypeVar("T", bound="V1Precondition")


@_attrs_define
class V1Precondition:
    """Precondition specifies how and the existence or absence of certain
    relationships as expressed through the accompanying filter should affect
    whether or not the operation proceeds.

    MUST_NOT_MATCH will fail the parent request if any relationships match the
    relationships filter.
    MUST_MATCH will fail the parent request if there are no
    relationships that match the filter.

        Attributes:
            operation (Union[Unset, V1PreconditionOperation]):  Default: V1PreconditionOperation.OPERATION_UNSPECIFIED.
            filter_ (Union[Unset, V1RelationshipFilter]): RelationshipFilter is a collection of filters which when applied
                to a
                relationship will return relationships that have exactly matching fields.

                resource_type is required. All other fields are optional and if left
                unspecified will not filter relationships.
    """

    operation: Union[Unset, V1PreconditionOperation] = V1PreconditionOperation.OPERATION_UNSPECIFIED
    filter_: Union[Unset, "V1RelationshipFilter"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        operation: Union[Unset, str] = UNSET
        if not isinstance(self.operation, Unset):
            operation = self.operation.value

        filter_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if operation is not UNSET:
            field_dict["operation"] = operation
        if filter_ is not UNSET:
            field_dict["filter"] = filter_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_relationship_filter import V1RelationshipFilter

        d = src_dict.copy()
        _operation = d.pop("operation", UNSET)
        operation: Union[Unset, V1PreconditionOperation]
        if isinstance(_operation, Unset):
            operation = UNSET
        else:
            operation = V1PreconditionOperation(_operation)

        _filter_ = d.pop("filter", UNSET)
        filter_: Union[Unset, V1RelationshipFilter]
        if isinstance(_filter_, Unset):
            filter_ = UNSET
        else:
            filter_ = V1RelationshipFilter.from_dict(_filter_)

        v1_precondition = cls(
            operation=operation,
            filter_=filter_,
        )

        v1_precondition.additional_properties = d
        return v1_precondition

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
