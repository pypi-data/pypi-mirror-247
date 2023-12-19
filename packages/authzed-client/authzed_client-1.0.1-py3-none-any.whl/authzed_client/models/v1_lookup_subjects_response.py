from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v1_lookup_permissionship import V1LookupPermissionship
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_cursor import V1Cursor
    from ..models.v1_partial_caveat_info import V1PartialCaveatInfo
    from ..models.v1_resolved_subject import V1ResolvedSubject
    from ..models.v1_zed_token import V1ZedToken


T = TypeVar("T", bound="V1LookupSubjectsResponse")


@_attrs_define
class V1LookupSubjectsResponse:
    """LookupSubjectsResponse contains a single matching subject object ID for the
    requested subject object type on the permission or relation.

        Attributes:
            looked_up_at (Union[Unset, V1ZedToken]): ZedToken is used to provide causality metadata between Write and Check
                requests.

                See the authzed.api.v1.Consistency message for more information.
            subject_object_id (Union[Unset, str]):
            excluded_subject_ids (Union[Unset, List[str]]):
            permissionship (Union[Unset, V1LookupPermissionship]): LookupPermissionship represents whether a Lookup response
                was partially evaluated or not Default: V1LookupPermissionship.LOOKUP_PERMISSIONSHIP_UNSPECIFIED.
            partial_caveat_info (Union[Unset, V1PartialCaveatInfo]): PartialCaveatInfo carries information necessary for the
                client to take action
                in the event a response contains a partially evaluated caveat
            subject (Union[Unset, V1ResolvedSubject]): ResolvedSubject is a single subject resolved within LookupSubjects.
            excluded_subjects (Union[Unset, List['V1ResolvedSubject']]): excluded_subjects are the subjects excluded. This
                list
                will only contain subjects if `subject.subject_object_id` is a wildcard (`*`) and
                will only be populated if exclusions exist from the wildcard.
            after_result_cursor (Union[Unset, V1Cursor]): Cursor is used to provide resumption of listing between calls to
                APIs
                such as LookupResources.
    """

    looked_up_at: Union[Unset, "V1ZedToken"] = UNSET
    subject_object_id: Union[Unset, str] = UNSET
    excluded_subject_ids: Union[Unset, List[str]] = UNSET
    permissionship: Union[Unset, V1LookupPermissionship] = V1LookupPermissionship.LOOKUP_PERMISSIONSHIP_UNSPECIFIED
    partial_caveat_info: Union[Unset, "V1PartialCaveatInfo"] = UNSET
    subject: Union[Unset, "V1ResolvedSubject"] = UNSET
    excluded_subjects: Union[Unset, List["V1ResolvedSubject"]] = UNSET
    after_result_cursor: Union[Unset, "V1Cursor"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        looked_up_at: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.looked_up_at, Unset):
            looked_up_at = self.looked_up_at.to_dict()

        subject_object_id = self.subject_object_id
        excluded_subject_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.excluded_subject_ids, Unset):
            excluded_subject_ids = self.excluded_subject_ids

        permissionship: Union[Unset, str] = UNSET
        if not isinstance(self.permissionship, Unset):
            permissionship = self.permissionship.value

        partial_caveat_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.partial_caveat_info, Unset):
            partial_caveat_info = self.partial_caveat_info.to_dict()

        subject: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.subject, Unset):
            subject = self.subject.to_dict()

        excluded_subjects: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.excluded_subjects, Unset):
            excluded_subjects = []
            for excluded_subjects_item_data in self.excluded_subjects:
                excluded_subjects_item = excluded_subjects_item_data.to_dict()

                excluded_subjects.append(excluded_subjects_item)

        after_result_cursor: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.after_result_cursor, Unset):
            after_result_cursor = self.after_result_cursor.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if looked_up_at is not UNSET:
            field_dict["lookedUpAt"] = looked_up_at
        if subject_object_id is not UNSET:
            field_dict["subjectObjectId"] = subject_object_id
        if excluded_subject_ids is not UNSET:
            field_dict["excludedSubjectIds"] = excluded_subject_ids
        if permissionship is not UNSET:
            field_dict["permissionship"] = permissionship
        if partial_caveat_info is not UNSET:
            field_dict["partialCaveatInfo"] = partial_caveat_info
        if subject is not UNSET:
            field_dict["subject"] = subject
        if excluded_subjects is not UNSET:
            field_dict["excludedSubjects"] = excluded_subjects
        if after_result_cursor is not UNSET:
            field_dict["afterResultCursor"] = after_result_cursor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_cursor import V1Cursor
        from ..models.v1_partial_caveat_info import V1PartialCaveatInfo
        from ..models.v1_resolved_subject import V1ResolvedSubject
        from ..models.v1_zed_token import V1ZedToken

        d = src_dict.copy()
        _looked_up_at = d.pop("lookedUpAt", UNSET)
        looked_up_at: Union[Unset, V1ZedToken]
        if isinstance(_looked_up_at, Unset):
            looked_up_at = UNSET
        else:
            looked_up_at = V1ZedToken.from_dict(_looked_up_at)

        subject_object_id = d.pop("subjectObjectId", UNSET)

        excluded_subject_ids = cast(List[str], d.pop("excludedSubjectIds", UNSET))

        _permissionship = d.pop("permissionship", UNSET)
        permissionship: Union[Unset, V1LookupPermissionship]
        if isinstance(_permissionship, Unset):
            permissionship = UNSET
        else:
            permissionship = V1LookupPermissionship(_permissionship)

        _partial_caveat_info = d.pop("partialCaveatInfo", UNSET)
        partial_caveat_info: Union[Unset, V1PartialCaveatInfo]
        if isinstance(_partial_caveat_info, Unset):
            partial_caveat_info = UNSET
        else:
            partial_caveat_info = V1PartialCaveatInfo.from_dict(_partial_caveat_info)

        _subject = d.pop("subject", UNSET)
        subject: Union[Unset, V1ResolvedSubject]
        if isinstance(_subject, Unset):
            subject = UNSET
        else:
            subject = V1ResolvedSubject.from_dict(_subject)

        excluded_subjects = []
        _excluded_subjects = d.pop("excludedSubjects", UNSET)
        for excluded_subjects_item_data in _excluded_subjects or []:
            excluded_subjects_item = V1ResolvedSubject.from_dict(excluded_subjects_item_data)

            excluded_subjects.append(excluded_subjects_item)

        _after_result_cursor = d.pop("afterResultCursor", UNSET)
        after_result_cursor: Union[Unset, V1Cursor]
        if isinstance(_after_result_cursor, Unset):
            after_result_cursor = UNSET
        else:
            after_result_cursor = V1Cursor.from_dict(_after_result_cursor)

        v1_lookup_subjects_response = cls(
            looked_up_at=looked_up_at,
            subject_object_id=subject_object_id,
            excluded_subject_ids=excluded_subject_ids,
            permissionship=permissionship,
            partial_caveat_info=partial_caveat_info,
            subject=subject,
            excluded_subjects=excluded_subjects,
            after_result_cursor=after_result_cursor,
        )

        v1_lookup_subjects_response.additional_properties = d
        return v1_lookup_subjects_response

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
