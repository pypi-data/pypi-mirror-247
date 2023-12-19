from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v1_bulk_import_relationships_request import V1BulkImportRelationshipsRequest
from ...models.v1_bulk_import_relationships_response import V1BulkImportRelationshipsResponse
from ...types import Response


def _get_kwargs(
    *,
    json_body: V1BulkImportRelationshipsRequest,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v1/experimental/relationships/bulkimport",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V1BulkImportRelationshipsResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = V1BulkImportRelationshipsResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V1BulkImportRelationshipsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1BulkImportRelationshipsRequest,
) -> Response[V1BulkImportRelationshipsResponse]:
    """BulkImportRelationships is a faster path to writing a large number of
    relationships at once. It is both batched and streaming. For maximum
    performance, the caller should attempt to write relationships in as close
    to relationship sort order as possible: (resource.object_type,
    resource.object_id, relation, subject.object.object_type,
    subject.object.object_id, subject.optional_relation)

     EXPERIMENTAL
    https://github.com/authzed/spicedb/issues/1303

    Args:
        json_body (V1BulkImportRelationshipsRequest): BulkImportRelationshipsRequest represents
            one batch of the streaming
            BulkImportRelationships API. The maximum size is only limited by the backing
            datastore, and optimal size should be determined by the calling client
            experimentally.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1BulkImportRelationshipsResponse]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1BulkImportRelationshipsRequest,
) -> Optional[V1BulkImportRelationshipsResponse]:
    """BulkImportRelationships is a faster path to writing a large number of
    relationships at once. It is both batched and streaming. For maximum
    performance, the caller should attempt to write relationships in as close
    to relationship sort order as possible: (resource.object_type,
    resource.object_id, relation, subject.object.object_type,
    subject.object.object_id, subject.optional_relation)

     EXPERIMENTAL
    https://github.com/authzed/spicedb/issues/1303

    Args:
        json_body (V1BulkImportRelationshipsRequest): BulkImportRelationshipsRequest represents
            one batch of the streaming
            BulkImportRelationships API. The maximum size is only limited by the backing
            datastore, and optimal size should be determined by the calling client
            experimentally.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1BulkImportRelationshipsResponse
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1BulkImportRelationshipsRequest,
) -> Response[V1BulkImportRelationshipsResponse]:
    """BulkImportRelationships is a faster path to writing a large number of
    relationships at once. It is both batched and streaming. For maximum
    performance, the caller should attempt to write relationships in as close
    to relationship sort order as possible: (resource.object_type,
    resource.object_id, relation, subject.object.object_type,
    subject.object.object_id, subject.optional_relation)

     EXPERIMENTAL
    https://github.com/authzed/spicedb/issues/1303

    Args:
        json_body (V1BulkImportRelationshipsRequest): BulkImportRelationshipsRequest represents
            one batch of the streaming
            BulkImportRelationships API. The maximum size is only limited by the backing
            datastore, and optimal size should be determined by the calling client
            experimentally.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1BulkImportRelationshipsResponse]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1BulkImportRelationshipsRequest,
) -> Optional[V1BulkImportRelationshipsResponse]:
    """BulkImportRelationships is a faster path to writing a large number of
    relationships at once. It is both batched and streaming. For maximum
    performance, the caller should attempt to write relationships in as close
    to relationship sort order as possible: (resource.object_type,
    resource.object_id, relation, subject.object.object_type,
    subject.object.object_id, subject.optional_relation)

     EXPERIMENTAL
    https://github.com/authzed/spicedb/issues/1303

    Args:
        json_body (V1BulkImportRelationshipsRequest): BulkImportRelationshipsRequest represents
            one batch of the streaming
            BulkImportRelationships API. The maximum size is only limited by the backing
            datastore, and optimal size should be determined by the calling client
            experimentally.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1BulkImportRelationshipsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
