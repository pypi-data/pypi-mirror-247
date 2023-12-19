from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_consistency import V1Consistency
    from ..models.v1_cursor import V1Cursor
    from ..models.v1_lookup_resources_request_context_consists_of_named_values_that_are_injected_into_the_caveat_evaluation_context import (
        V1LookupResourcesRequestContextConsistsOfNamedValuesThatAreInjectedIntoTheCaveatEvaluationContext,
    )
    from ..models.v1_subject_reference import V1SubjectReference


T = TypeVar("T", bound="V1LookupResourcesRequest")


@_attrs_define
class V1LookupResourcesRequest:
    """LookupResourcesRequest performs a lookup of all resources of a particular
    kind on which the subject has the specified permission or the relation in
    which the subject exists, streaming back the IDs of those resources.

        Attributes:
            consistency (Union[Unset, V1Consistency]): Consistency will define how a request is handled by the backend.
                By defining a consistency requirement, and a token at which those
                requirements should be applied, where applicable.
            resource_object_type (Union[Unset, str]): resource_object_type is the type of resource object for which the IDs
                will
                be returned.
            permission (Union[Unset, str]): permission is the name of the permission or relation for which the subject
                must Check.
            subject (Union[Unset, V1SubjectReference]): SubjectReference is used for referring to the subject portion of a
                Relationship. The relation component is optional and is used for defining a
                sub-relation on the subject, e.g. group:123#members
            context (Union[Unset,
                V1LookupResourcesRequestContextConsistsOfNamedValuesThatAreInjectedIntoTheCaveatEvaluationContext]):
            optional_limit (Union[Unset, int]): optional_limit, if non-zero, specifies the limit on the number of resources
                to return
                before the stream is closed on the server side. By default, the stream will continue
                resolving resources until exhausted or the stream is closed due to the client or a
                network issue.
            optional_cursor (Union[Unset, V1Cursor]): Cursor is used to provide resumption of listing between calls to APIs
                such as LookupResources.
    """

    consistency: Union[Unset, "V1Consistency"] = UNSET
    resource_object_type: Union[Unset, str] = UNSET
    permission: Union[Unset, str] = UNSET
    subject: Union[Unset, "V1SubjectReference"] = UNSET
    context: Union[
        Unset, "V1LookupResourcesRequestContextConsistsOfNamedValuesThatAreInjectedIntoTheCaveatEvaluationContext"
    ] = UNSET
    optional_limit: Union[Unset, int] = UNSET
    optional_cursor: Union[Unset, "V1Cursor"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        consistency: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.consistency, Unset):
            consistency = self.consistency.to_dict()

        resource_object_type = self.resource_object_type
        permission = self.permission
        subject: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.subject, Unset):
            subject = self.subject.to_dict()

        context: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        optional_limit = self.optional_limit
        optional_cursor: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.optional_cursor, Unset):
            optional_cursor = self.optional_cursor.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if consistency is not UNSET:
            field_dict["consistency"] = consistency
        if resource_object_type is not UNSET:
            field_dict["resourceObjectType"] = resource_object_type
        if permission is not UNSET:
            field_dict["permission"] = permission
        if subject is not UNSET:
            field_dict["subject"] = subject
        if context is not UNSET:
            field_dict["context"] = context
        if optional_limit is not UNSET:
            field_dict["optionalLimit"] = optional_limit
        if optional_cursor is not UNSET:
            field_dict["optionalCursor"] = optional_cursor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_consistency import V1Consistency
        from ..models.v1_cursor import V1Cursor
        from ..models.v1_lookup_resources_request_context_consists_of_named_values_that_are_injected_into_the_caveat_evaluation_context import (
            V1LookupResourcesRequestContextConsistsOfNamedValuesThatAreInjectedIntoTheCaveatEvaluationContext,
        )
        from ..models.v1_subject_reference import V1SubjectReference

        d = src_dict.copy()
        _consistency = d.pop("consistency", UNSET)
        consistency: Union[Unset, V1Consistency]
        if isinstance(_consistency, Unset):
            consistency = UNSET
        else:
            consistency = V1Consistency.from_dict(_consistency)

        resource_object_type = d.pop("resourceObjectType", UNSET)

        permission = d.pop("permission", UNSET)

        _subject = d.pop("subject", UNSET)
        subject: Union[Unset, V1SubjectReference]
        if isinstance(_subject, Unset):
            subject = UNSET
        else:
            subject = V1SubjectReference.from_dict(_subject)

        _context = d.pop("context", UNSET)
        context: Union[
            Unset, V1LookupResourcesRequestContextConsistsOfNamedValuesThatAreInjectedIntoTheCaveatEvaluationContext
        ]
        if isinstance(_context, Unset):
            context = UNSET
        else:
            context = V1LookupResourcesRequestContextConsistsOfNamedValuesThatAreInjectedIntoTheCaveatEvaluationContext.from_dict(
                _context
            )

        optional_limit = d.pop("optionalLimit", UNSET)

        _optional_cursor = d.pop("optionalCursor", UNSET)
        optional_cursor: Union[Unset, V1Cursor]
        if isinstance(_optional_cursor, Unset):
            optional_cursor = UNSET
        else:
            optional_cursor = V1Cursor.from_dict(_optional_cursor)

        v1_lookup_resources_request = cls(
            consistency=consistency,
            resource_object_type=resource_object_type,
            permission=permission,
            subject=subject,
            context=context,
            optional_limit=optional_limit,
            optional_cursor=optional_cursor,
        )

        v1_lookup_resources_request.additional_properties = d
        return v1_lookup_resources_request

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
