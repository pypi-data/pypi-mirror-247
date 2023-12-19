from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.apiv_1_write_schema_request import Apiv1WriteSchemaRequest
from ...models.apiv_1_write_schema_response import Apiv1WriteSchemaResponse
from ...types import Response


def _get_kwargs(
    *,
    json_body: Apiv1WriteSchemaRequest,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v1/schema/write",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Apiv1WriteSchemaResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Apiv1WriteSchemaResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Apiv1WriteSchemaResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: Apiv1WriteSchemaRequest,
) -> Response[Apiv1WriteSchemaResponse]:
    """Write overwrites the current Object Definitions for a Permissions System.

    Args:
        json_body (Apiv1WriteSchemaRequest): WriteSchemaRequest is the required data used to
            "upsert" the Schema of a
            Permissions System.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Apiv1WriteSchemaResponse]
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
    json_body: Apiv1WriteSchemaRequest,
) -> Optional[Apiv1WriteSchemaResponse]:
    """Write overwrites the current Object Definitions for a Permissions System.

    Args:
        json_body (Apiv1WriteSchemaRequest): WriteSchemaRequest is the required data used to
            "upsert" the Schema of a
            Permissions System.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Apiv1WriteSchemaResponse
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: Apiv1WriteSchemaRequest,
) -> Response[Apiv1WriteSchemaResponse]:
    """Write overwrites the current Object Definitions for a Permissions System.

    Args:
        json_body (Apiv1WriteSchemaRequest): WriteSchemaRequest is the required data used to
            "upsert" the Schema of a
            Permissions System.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Apiv1WriteSchemaResponse]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: Apiv1WriteSchemaRequest,
) -> Optional[Apiv1WriteSchemaResponse]:
    """Write overwrites the current Object Definitions for a Permissions System.

    Args:
        json_body (Apiv1WriteSchemaRequest): WriteSchemaRequest is the required data used to
            "upsert" the Schema of a
            Permissions System.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Apiv1WriteSchemaResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
