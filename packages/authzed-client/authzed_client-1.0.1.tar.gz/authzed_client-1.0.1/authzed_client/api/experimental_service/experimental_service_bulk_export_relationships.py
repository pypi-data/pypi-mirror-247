from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.experimental_service_bulk_export_relationships_stream_result_of_v1_bulk_export_relationships_response import (
    ExperimentalServiceBulkExportRelationshipsStreamResultOfV1BulkExportRelationshipsResponse,
)
from ...models.v1_bulk_export_relationships_request import V1BulkExportRelationshipsRequest
from ...types import Response


def _get_kwargs(
    *,
    json_body: V1BulkExportRelationshipsRequest,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v1/experimental/relationships/bulkexport",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ExperimentalServiceBulkExportRelationshipsStreamResultOfV1BulkExportRelationshipsResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = (
            ExperimentalServiceBulkExportRelationshipsStreamResultOfV1BulkExportRelationshipsResponse.from_dict(
                response.json()
            )
        )

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ExperimentalServiceBulkExportRelationshipsStreamResultOfV1BulkExportRelationshipsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1BulkExportRelationshipsRequest,
) -> Response[ExperimentalServiceBulkExportRelationshipsStreamResultOfV1BulkExportRelationshipsResponse]:
    """BulkExportRelationships is the fastest path available to exporting
    relationships from the server. It is resumable, and will return results
    in an order determined by the server.

    Args:
        json_body (V1BulkExportRelationshipsRequest): BulkExportRelationshipsRequest represents a
            resumable request for
            all relationships from the server.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExperimentalServiceBulkExportRelationshipsStreamResultOfV1BulkExportRelationshipsResponse]
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
    json_body: V1BulkExportRelationshipsRequest,
) -> Optional[ExperimentalServiceBulkExportRelationshipsStreamResultOfV1BulkExportRelationshipsResponse]:
    """BulkExportRelationships is the fastest path available to exporting
    relationships from the server. It is resumable, and will return results
    in an order determined by the server.

    Args:
        json_body (V1BulkExportRelationshipsRequest): BulkExportRelationshipsRequest represents a
            resumable request for
            all relationships from the server.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExperimentalServiceBulkExportRelationshipsStreamResultOfV1BulkExportRelationshipsResponse
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1BulkExportRelationshipsRequest,
) -> Response[ExperimentalServiceBulkExportRelationshipsStreamResultOfV1BulkExportRelationshipsResponse]:
    """BulkExportRelationships is the fastest path available to exporting
    relationships from the server. It is resumable, and will return results
    in an order determined by the server.

    Args:
        json_body (V1BulkExportRelationshipsRequest): BulkExportRelationshipsRequest represents a
            resumable request for
            all relationships from the server.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExperimentalServiceBulkExportRelationshipsStreamResultOfV1BulkExportRelationshipsResponse]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1BulkExportRelationshipsRequest,
) -> Optional[ExperimentalServiceBulkExportRelationshipsStreamResultOfV1BulkExportRelationshipsResponse]:
    """BulkExportRelationships is the fastest path available to exporting
    relationships from the server. It is resumable, and will return results
    in an order determined by the server.

    Args:
        json_body (V1BulkExportRelationshipsRequest): BulkExportRelationshipsRequest represents a
            resumable request for
            all relationships from the server.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExperimentalServiceBulkExportRelationshipsStreamResultOfV1BulkExportRelationshipsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
