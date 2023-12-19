from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v1_bulk_check_permission_request import V1BulkCheckPermissionRequest
from ...models.v1_bulk_check_permission_response import V1BulkCheckPermissionResponse
from ...types import Response


def _get_kwargs(
    *,
    json_body: V1BulkCheckPermissionRequest,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v1/experimental/permissions/bulkcheckpermission",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V1BulkCheckPermissionResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = V1BulkCheckPermissionResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V1BulkCheckPermissionResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1BulkCheckPermissionRequest,
) -> Response[V1BulkCheckPermissionResponse]:
    """
    Args:
        json_body (V1BulkCheckPermissionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1BulkCheckPermissionResponse]
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
    json_body: V1BulkCheckPermissionRequest,
) -> Optional[V1BulkCheckPermissionResponse]:
    """
    Args:
        json_body (V1BulkCheckPermissionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1BulkCheckPermissionResponse
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1BulkCheckPermissionRequest,
) -> Response[V1BulkCheckPermissionResponse]:
    """
    Args:
        json_body (V1BulkCheckPermissionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1BulkCheckPermissionResponse]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1BulkCheckPermissionRequest,
) -> Optional[V1BulkCheckPermissionResponse]:
    """
    Args:
        json_body (V1BulkCheckPermissionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1BulkCheckPermissionResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
