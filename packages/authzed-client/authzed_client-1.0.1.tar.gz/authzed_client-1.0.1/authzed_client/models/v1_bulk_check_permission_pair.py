from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rpc_status import RpcStatus
    from ..models.v1_bulk_check_permission_request_item import V1BulkCheckPermissionRequestItem
    from ..models.v1_bulk_check_permission_response_item import V1BulkCheckPermissionResponseItem


T = TypeVar("T", bound="V1BulkCheckPermissionPair")


@_attrs_define
class V1BulkCheckPermissionPair:
    """
    Attributes:
        request (Union[Unset, V1BulkCheckPermissionRequestItem]):
        item (Union[Unset, V1BulkCheckPermissionResponseItem]):
        error (Union[Unset, RpcStatus]): The `Status` type defines a logical error model that is suitable for
            different programming environments, including REST APIs and RPC APIs. It is
            used by [gRPC](https://github.com/grpc). Each `Status` message contains
            three pieces of data: error code, error message, and error details.

            You can find out more about this error model and how to work with it in the
            [API Design Guide](https://cloud.google.com/apis/design/errors).
    """

    request: Union[Unset, "V1BulkCheckPermissionRequestItem"] = UNSET
    item: Union[Unset, "V1BulkCheckPermissionResponseItem"] = UNSET
    error: Union[Unset, "RpcStatus"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.request, Unset):
            request = self.request.to_dict()

        item: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.item, Unset):
            item = self.item.to_dict()

        error: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if request is not UNSET:
            field_dict["request"] = request
        if item is not UNSET:
            field_dict["item"] = item
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.rpc_status import RpcStatus
        from ..models.v1_bulk_check_permission_request_item import V1BulkCheckPermissionRequestItem
        from ..models.v1_bulk_check_permission_response_item import V1BulkCheckPermissionResponseItem

        d = src_dict.copy()
        _request = d.pop("request", UNSET)
        request: Union[Unset, V1BulkCheckPermissionRequestItem]
        if isinstance(_request, Unset):
            request = UNSET
        else:
            request = V1BulkCheckPermissionRequestItem.from_dict(_request)

        _item = d.pop("item", UNSET)
        item: Union[Unset, V1BulkCheckPermissionResponseItem]
        if isinstance(_item, Unset):
            item = UNSET
        else:
            item = V1BulkCheckPermissionResponseItem.from_dict(_item)

        _error = d.pop("error", UNSET)
        error: Union[Unset, RpcStatus]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = RpcStatus.from_dict(_error)

        v1_bulk_check_permission_pair = cls(
            request=request,
            item=item,
            error=error,
        )

        v1_bulk_check_permission_pair.additional_properties = d
        return v1_bulk_check_permission_pair

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
