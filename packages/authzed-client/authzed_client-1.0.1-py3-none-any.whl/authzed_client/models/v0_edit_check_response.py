from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0_developer_error import V0DeveloperError
    from ..models.v0_edit_check_result import V0EditCheckResult


T = TypeVar("T", bound="V0EditCheckResponse")


@_attrs_define
class V0EditCheckResponse:
    """
    Attributes:
        request_errors (Union[Unset, List['V0DeveloperError']]):
        check_results (Union[Unset, List['V0EditCheckResult']]):
    """

    request_errors: Union[Unset, List["V0DeveloperError"]] = UNSET
    check_results: Union[Unset, List["V0EditCheckResult"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_errors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.request_errors, Unset):
            request_errors = []
            for request_errors_item_data in self.request_errors:
                request_errors_item = request_errors_item_data.to_dict()

                request_errors.append(request_errors_item)

        check_results: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.check_results, Unset):
            check_results = []
            for check_results_item_data in self.check_results:
                check_results_item = check_results_item_data.to_dict()

                check_results.append(check_results_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if request_errors is not UNSET:
            field_dict["requestErrors"] = request_errors
        if check_results is not UNSET:
            field_dict["checkResults"] = check_results

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v0_developer_error import V0DeveloperError
        from ..models.v0_edit_check_result import V0EditCheckResult

        d = src_dict.copy()
        request_errors = []
        _request_errors = d.pop("requestErrors", UNSET)
        for request_errors_item_data in _request_errors or []:
            request_errors_item = V0DeveloperError.from_dict(request_errors_item_data)

            request_errors.append(request_errors_item)

        check_results = []
        _check_results = d.pop("checkResults", UNSET)
        for check_results_item_data in _check_results or []:
            check_results_item = V0EditCheckResult.from_dict(check_results_item_data)

            check_results.append(check_results_item)

        v0_edit_check_response = cls(
            request_errors=request_errors,
            check_results=check_results,
        )

        v0_edit_check_response.additional_properties = d
        return v0_edit_check_response

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
