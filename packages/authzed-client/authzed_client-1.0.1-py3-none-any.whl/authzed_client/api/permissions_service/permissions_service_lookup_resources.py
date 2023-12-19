from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.permissions_service_lookup_resources_stream_result_of_v1_lookup_resources_response import (
    PermissionsServiceLookupResourcesStreamResultOfV1LookupResourcesResponse,
)
from ...models.v1_lookup_resources_request import V1LookupResourcesRequest
from ...types import Response


def _get_kwargs(
    *,
    json_body: V1LookupResourcesRequest,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v1/permissions/resources",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[PermissionsServiceLookupResourcesStreamResultOfV1LookupResourcesResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PermissionsServiceLookupResourcesStreamResultOfV1LookupResourcesResponse.from_dict(
            response.json()
        )

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PermissionsServiceLookupResourcesStreamResultOfV1LookupResourcesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1LookupResourcesRequest,
) -> Response[PermissionsServiceLookupResourcesStreamResultOfV1LookupResourcesResponse]:
    """LookupResources returns all the resources of a given type that a subject
    can access whether via a computed permission or relation membership.

    Args:
        json_body (V1LookupResourcesRequest): LookupResourcesRequest performs a lookup of all
            resources of a particular
            kind on which the subject has the specified permission or the relation in
            which the subject exists, streaming back the IDs of those resources.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PermissionsServiceLookupResourcesStreamResultOfV1LookupResourcesResponse]
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
    json_body: V1LookupResourcesRequest,
) -> Optional[PermissionsServiceLookupResourcesStreamResultOfV1LookupResourcesResponse]:
    """LookupResources returns all the resources of a given type that a subject
    can access whether via a computed permission or relation membership.

    Args:
        json_body (V1LookupResourcesRequest): LookupResourcesRequest performs a lookup of all
            resources of a particular
            kind on which the subject has the specified permission or the relation in
            which the subject exists, streaming back the IDs of those resources.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PermissionsServiceLookupResourcesStreamResultOfV1LookupResourcesResponse
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1LookupResourcesRequest,
) -> Response[PermissionsServiceLookupResourcesStreamResultOfV1LookupResourcesResponse]:
    """LookupResources returns all the resources of a given type that a subject
    can access whether via a computed permission or relation membership.

    Args:
        json_body (V1LookupResourcesRequest): LookupResourcesRequest performs a lookup of all
            resources of a particular
            kind on which the subject has the specified permission or the relation in
            which the subject exists, streaming back the IDs of those resources.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PermissionsServiceLookupResourcesStreamResultOfV1LookupResourcesResponse]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1LookupResourcesRequest,
) -> Optional[PermissionsServiceLookupResourcesStreamResultOfV1LookupResourcesResponse]:
    """LookupResources returns all the resources of a given type that a subject
    can access whether via a computed permission or relation membership.

    Args:
        json_body (V1LookupResourcesRequest): LookupResourcesRequest performs a lookup of all
            resources of a particular
            kind on which the subject has the specified permission or the relation in
            which the subject exists, streaming back the IDs of those resources.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PermissionsServiceLookupResourcesStreamResultOfV1LookupResourcesResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
