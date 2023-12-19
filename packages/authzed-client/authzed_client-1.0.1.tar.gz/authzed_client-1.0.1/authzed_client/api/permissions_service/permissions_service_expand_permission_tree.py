from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v1_expand_permission_tree_request import V1ExpandPermissionTreeRequest
from ...models.v1_expand_permission_tree_response import V1ExpandPermissionTreeResponse
from ...types import Response


def _get_kwargs(
    *,
    json_body: V1ExpandPermissionTreeRequest,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v1/permissions/expand",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V1ExpandPermissionTreeResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = V1ExpandPermissionTreeResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V1ExpandPermissionTreeResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1ExpandPermissionTreeRequest,
) -> Response[V1ExpandPermissionTreeResponse]:
    """ExpandPermissionTree reveals the graph structure for a resource's
    permission or relation. This RPC does not recurse infinitely deep and may
    require multiple calls to fully unnest a deeply nested graph.

    Args:
        json_body (V1ExpandPermissionTreeRequest): ExpandPermissionTreeRequest returns a tree
            representing the expansion of all
            relationships found accessible from a permission or relation on a particular
            resource.

            ExpandPermissionTreeRequest is typically used to determine the full set of
            subjects with a permission, along with the relationships that grant said
            access.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1ExpandPermissionTreeResponse]
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
    json_body: V1ExpandPermissionTreeRequest,
) -> Optional[V1ExpandPermissionTreeResponse]:
    """ExpandPermissionTree reveals the graph structure for a resource's
    permission or relation. This RPC does not recurse infinitely deep and may
    require multiple calls to fully unnest a deeply nested graph.

    Args:
        json_body (V1ExpandPermissionTreeRequest): ExpandPermissionTreeRequest returns a tree
            representing the expansion of all
            relationships found accessible from a permission or relation on a particular
            resource.

            ExpandPermissionTreeRequest is typically used to determine the full set of
            subjects with a permission, along with the relationships that grant said
            access.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1ExpandPermissionTreeResponse
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1ExpandPermissionTreeRequest,
) -> Response[V1ExpandPermissionTreeResponse]:
    """ExpandPermissionTree reveals the graph structure for a resource's
    permission or relation. This RPC does not recurse infinitely deep and may
    require multiple calls to fully unnest a deeply nested graph.

    Args:
        json_body (V1ExpandPermissionTreeRequest): ExpandPermissionTreeRequest returns a tree
            representing the expansion of all
            relationships found accessible from a permission or relation on a particular
            resource.

            ExpandPermissionTreeRequest is typically used to determine the full set of
            subjects with a permission, along with the relationships that grant said
            access.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1ExpandPermissionTreeResponse]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V1ExpandPermissionTreeRequest,
) -> Optional[V1ExpandPermissionTreeResponse]:
    """ExpandPermissionTree reveals the graph structure for a resource's
    permission or relation. This RPC does not recurse infinitely deep and may
    require multiple calls to fully unnest a deeply nested graph.

    Args:
        json_body (V1ExpandPermissionTreeRequest): ExpandPermissionTreeRequest returns a tree
            representing the expansion of all
            relationships found accessible from a permission or relation on a particular
            resource.

            ExpandPermissionTreeRequest is typically used to determine the full set of
            subjects with a permission, along with the relationships that grant said
            access.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1ExpandPermissionTreeResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
