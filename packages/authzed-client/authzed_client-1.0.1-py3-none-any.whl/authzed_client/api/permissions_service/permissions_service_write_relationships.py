from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v1_write_relationships_request import V1WriteRelationshipsRequest
from ...models.v1_write_relationships_response import V1WriteRelationshipsResponse
from ...types import Response


def _get_kwargs(
    *,
    json_body: V1WriteRelationshipsRequest,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v1/relationships/write",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V1WriteRelationshipsResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = V1WriteRelationshipsResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V1WriteRelationshipsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1WriteRelationshipsRequest,
) -> Response[V1WriteRelationshipsResponse]:
    """WriteRelationships atomically writes and/or deletes a set of specified
    relationships. An optional set of preconditions can be provided that must
    be satisfied for the operation to commit.

    Args:
        json_body (V1WriteRelationshipsRequest): WriteRelationshipsRequest contains a list of
            Relationship mutations that
            should be applied to the service. If the optional_preconditions parameter
            is included, all of the specified preconditions must also be satisfied before
            the write will be committed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1WriteRelationshipsResponse]
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
    json_body: V1WriteRelationshipsRequest,
) -> Optional[V1WriteRelationshipsResponse]:
    """WriteRelationships atomically writes and/or deletes a set of specified
    relationships. An optional set of preconditions can be provided that must
    be satisfied for the operation to commit.

    Args:
        json_body (V1WriteRelationshipsRequest): WriteRelationshipsRequest contains a list of
            Relationship mutations that
            should be applied to the service. If the optional_preconditions parameter
            is included, all of the specified preconditions must also be satisfied before
            the write will be committed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1WriteRelationshipsResponse
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1WriteRelationshipsRequest,
) -> Response[V1WriteRelationshipsResponse]:
    """WriteRelationships atomically writes and/or deletes a set of specified
    relationships. An optional set of preconditions can be provided that must
    be satisfied for the operation to commit.

    Args:
        json_body (V1WriteRelationshipsRequest): WriteRelationshipsRequest contains a list of
            Relationship mutations that
            should be applied to the service. If the optional_preconditions parameter
            is included, all of the specified preconditions must also be satisfied before
            the write will be committed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1WriteRelationshipsResponse]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1WriteRelationshipsRequest,
) -> Optional[V1WriteRelationshipsResponse]:
    """WriteRelationships atomically writes and/or deletes a set of specified
    relationships. An optional set of preconditions can be provided that must
    be satisfied for the operation to commit.

    Args:
        json_body (V1WriteRelationshipsRequest): WriteRelationshipsRequest contains a list of
            Relationship mutations that
            should be applied to the service. If the optional_preconditions parameter
            is included, all of the specified preconditions must also be satisfied before
            the write will be committed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1WriteRelationshipsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
