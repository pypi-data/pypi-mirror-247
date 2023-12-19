from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_zed_token import V1ZedToken


T = TypeVar("T", bound="V1Consistency")


@_attrs_define
class V1Consistency:
    """Consistency will define how a request is handled by the backend.
    By defining a consistency requirement, and a token at which those
    requirements should be applied, where applicable.

        Attributes:
            minimize_latency (Union[Unset, bool]): minimize_latency indicates that the latency for the call should be
                minimized by having the system select the fastest snapshot available.
            at_least_as_fresh (Union[Unset, V1ZedToken]): ZedToken is used to provide causality metadata between Write and
                Check
                requests.

                See the authzed.api.v1.Consistency message for more information.
            at_exact_snapshot (Union[Unset, V1ZedToken]): ZedToken is used to provide causality metadata between Write and
                Check
                requests.

                See the authzed.api.v1.Consistency message for more information.
            fully_consistent (Union[Unset, bool]): fully_consistent indicates that all data used in the API call *must* be
                at the most recent snapshot found.

                NOTE: using this method can be *quite slow*, so unless there is a need to
                do so, it is recommended to use `at_least_as_fresh` with a stored
                ZedToken.
    """

    minimize_latency: Union[Unset, bool] = UNSET
    at_least_as_fresh: Union[Unset, "V1ZedToken"] = UNSET
    at_exact_snapshot: Union[Unset, "V1ZedToken"] = UNSET
    fully_consistent: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        minimize_latency = self.minimize_latency
        at_least_as_fresh: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.at_least_as_fresh, Unset):
            at_least_as_fresh = self.at_least_as_fresh.to_dict()

        at_exact_snapshot: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.at_exact_snapshot, Unset):
            at_exact_snapshot = self.at_exact_snapshot.to_dict()

        fully_consistent = self.fully_consistent

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if minimize_latency is not UNSET:
            field_dict["minimizeLatency"] = minimize_latency
        if at_least_as_fresh is not UNSET:
            field_dict["atLeastAsFresh"] = at_least_as_fresh
        if at_exact_snapshot is not UNSET:
            field_dict["atExactSnapshot"] = at_exact_snapshot
        if fully_consistent is not UNSET:
            field_dict["fullyConsistent"] = fully_consistent

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_zed_token import V1ZedToken

        d = src_dict.copy()
        minimize_latency = d.pop("minimizeLatency", UNSET)

        _at_least_as_fresh = d.pop("atLeastAsFresh", UNSET)
        at_least_as_fresh: Union[Unset, V1ZedToken]
        if isinstance(_at_least_as_fresh, Unset):
            at_least_as_fresh = UNSET
        else:
            at_least_as_fresh = V1ZedToken.from_dict(_at_least_as_fresh)

        _at_exact_snapshot = d.pop("atExactSnapshot", UNSET)
        at_exact_snapshot: Union[Unset, V1ZedToken]
        if isinstance(_at_exact_snapshot, Unset):
            at_exact_snapshot = UNSET
        else:
            at_exact_snapshot = V1ZedToken.from_dict(_at_exact_snapshot)

        fully_consistent = d.pop("fullyConsistent", UNSET)

        v1_consistency = cls(
            minimize_latency=minimize_latency,
            at_least_as_fresh=at_least_as_fresh,
            at_exact_snapshot=at_exact_snapshot,
            fully_consistent=fully_consistent,
        )

        v1_consistency.additional_properties = d
        return v1_consistency

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
