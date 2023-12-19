from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v1_delete_relationships_request import V1DeleteRelationshipsRequest
from ...models.v1_delete_relationships_response import V1DeleteRelationshipsResponse
from ...types import Response


def _get_kwargs(
    *,
    json_body: V1DeleteRelationshipsRequest,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v1/relationships/delete",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V1DeleteRelationshipsResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = V1DeleteRelationshipsResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V1DeleteRelationshipsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1DeleteRelationshipsRequest,
) -> Response[V1DeleteRelationshipsResponse]:
    """DeleteRelationships atomically bulk deletes all relationships matching the
    provided filter. If no relationships match, none will be deleted and the
    operation will succeed. An optional set of preconditions can be provided that must
    be satisfied for the operation to commit.

    Args:
        json_body (V1DeleteRelationshipsRequest): DeleteRelationshipsRequest specifies which
            Relationships should be deleted,
            requesting the delete of *ALL* relationships that match the specified
            filters. If the optional_preconditions parameter is included, all of the
            specified preconditions must also be satisfied before the delete will be
            executed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1DeleteRelationshipsResponse]
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
    json_body: V1DeleteRelationshipsRequest,
) -> Optional[V1DeleteRelationshipsResponse]:
    """DeleteRelationships atomically bulk deletes all relationships matching the
    provided filter. If no relationships match, none will be deleted and the
    operation will succeed. An optional set of preconditions can be provided that must
    be satisfied for the operation to commit.

    Args:
        json_body (V1DeleteRelationshipsRequest): DeleteRelationshipsRequest specifies which
            Relationships should be deleted,
            requesting the delete of *ALL* relationships that match the specified
            filters. If the optional_preconditions parameter is included, all of the
            specified preconditions must also be satisfied before the delete will be
            executed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1DeleteRelationshipsResponse
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1DeleteRelationshipsRequest,
) -> Response[V1DeleteRelationshipsResponse]:
    """DeleteRelationships atomically bulk deletes all relationships matching the
    provided filter. If no relationships match, none will be deleted and the
    operation will succeed. An optional set of preconditions can be provided that must
    be satisfied for the operation to commit.

    Args:
        json_body (V1DeleteRelationshipsRequest): DeleteRelationshipsRequest specifies which
            Relationships should be deleted,
            requesting the delete of *ALL* relationships that match the specified
            filters. If the optional_preconditions parameter is included, all of the
            specified preconditions must also be satisfied before the delete will be
            executed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1DeleteRelationshipsResponse]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1DeleteRelationshipsRequest,
) -> Optional[V1DeleteRelationshipsResponse]:
    """DeleteRelationships atomically bulk deletes all relationships matching the
    provided filter. If no relationships match, none will be deleted and the
    operation will succeed. An optional set of preconditions can be provided that must
    be satisfied for the operation to commit.

    Args:
        json_body (V1DeleteRelationshipsRequest): DeleteRelationshipsRequest specifies which
            Relationships should be deleted,
            requesting the delete of *ALL* relationships that match the specified
            filters. If the optional_preconditions parameter is included, all of the
            specified preconditions must also be satisfied before the delete will be
            executed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1DeleteRelationshipsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
