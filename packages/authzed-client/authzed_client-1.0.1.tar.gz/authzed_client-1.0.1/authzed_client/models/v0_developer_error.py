from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.developer_error_error_kind import DeveloperErrorErrorKind
from ..models.developer_error_source import DeveloperErrorSource
from ..types import UNSET, Unset

T = TypeVar("T", bound="V0DeveloperError")


@_attrs_define
class V0DeveloperError:
    """
    Attributes:
        message (Union[Unset, str]):
        line (Union[Unset, int]):
        column (Union[Unset, int]):
        source (Union[Unset, DeveloperErrorSource]):  Default: DeveloperErrorSource.UNKNOWN_SOURCE.
        kind (Union[Unset, DeveloperErrorErrorKind]):  Default: DeveloperErrorErrorKind.UNKNOWN_KIND.
        path (Union[Unset, List[str]]):
        context (Union[Unset, str]): context holds the context for the error. For schema issues, this will be the
            name of the object type. For relationship issues, the full relationship string.
    """

    message: Union[Unset, str] = UNSET
    line: Union[Unset, int] = UNSET
    column: Union[Unset, int] = UNSET
    source: Union[Unset, DeveloperErrorSource] = DeveloperErrorSource.UNKNOWN_SOURCE
    kind: Union[Unset, DeveloperErrorErrorKind] = DeveloperErrorErrorKind.UNKNOWN_KIND
    path: Union[Unset, List[str]] = UNSET
    context: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        message = self.message
        line = self.line
        column = self.column
        source: Union[Unset, str] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        kind: Union[Unset, str] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        path: Union[Unset, List[str]] = UNSET
        if not isinstance(self.path, Unset):
            path = self.path

        context = self.context

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if line is not UNSET:
            field_dict["line"] = line
        if column is not UNSET:
            field_dict["column"] = column
        if source is not UNSET:
            field_dict["source"] = source
        if kind is not UNSET:
            field_dict["kind"] = kind
        if path is not UNSET:
            field_dict["path"] = path
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        message = d.pop("message", UNSET)

        line = d.pop("line", UNSET)

        column = d.pop("column", UNSET)

        _source = d.pop("source", UNSET)
        source: Union[Unset, DeveloperErrorSource]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = DeveloperErrorSource(_source)

        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, DeveloperErrorErrorKind]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = DeveloperErrorErrorKind(_kind)

        path = cast(List[str], d.pop("path", UNSET))

        context = d.pop("context", UNSET)

        v0_developer_error = cls(
            message=message,
            line=line,
            column=column,
            source=source,
            kind=kind,
            path=path,
            context=context,
        )

        v0_developer_error.additional_properties = d
        return v0_developer_error

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
