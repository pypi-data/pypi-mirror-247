from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rpc_status import RpcStatus
    from ..models.v1_watch_response import V1WatchResponse


T = TypeVar("T", bound="WatchServiceWatchStreamResultOfV1WatchResponse")


@_attrs_define
class WatchServiceWatchStreamResultOfV1WatchResponse:
    """
    Attributes:
        result (Union[Unset, V1WatchResponse]): WatchResponse contains all tuple modification events in ascending
            timestamp order, from the requested start snapshot to a snapshot
            encoded in the watch response. The client can use the snapshot to resume
            watching where the previous watch response left off.
        error (Union[Unset, RpcStatus]): The `Status` type defines a logical error model that is suitable for
            different programming environments, including REST APIs and RPC APIs. It is
            used by [gRPC](https://github.com/grpc). Each `Status` message contains
            three pieces of data: error code, error message, and error details.

            You can find out more about this error model and how to work with it in the
            [API Design Guide](https://cloud.google.com/apis/design/errors).
    """

    result: Union[Unset, "V1WatchResponse"] = UNSET
    error: Union[Unset, "RpcStatus"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        result: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.to_dict()

        error: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if result is not UNSET:
            field_dict["result"] = result
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.rpc_status import RpcStatus
        from ..models.v1_watch_response import V1WatchResponse

        d = src_dict.copy()
        _result = d.pop("result", UNSET)
        result: Union[Unset, V1WatchResponse]
        if isinstance(_result, Unset):
            result = UNSET
        else:
            result = V1WatchResponse.from_dict(_result)

        _error = d.pop("error", UNSET)
        error: Union[Unset, RpcStatus]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = RpcStatus.from_dict(_error)

        watch_service_watch_stream_result_of_v1_watch_response = cls(
            result=result,
            error=error,
        )

        watch_service_watch_stream_result_of_v1_watch_response.additional_properties = d
        return watch_service_watch_stream_result_of_v1_watch_response

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
