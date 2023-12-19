from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.apiv_1_read_schema_request import Apiv1ReadSchemaRequest
from ...models.apiv_1_read_schema_response import Apiv1ReadSchemaResponse
from ...types import Response


def _get_kwargs(
    *,
    json_body: Apiv1ReadSchemaRequest,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v1/schema/read",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Apiv1ReadSchemaResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Apiv1ReadSchemaResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Apiv1ReadSchemaResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: Apiv1ReadSchemaRequest,
) -> Response[Apiv1ReadSchemaResponse]:
    """Read returns the current Object Definitions for a Permissions System.

     Errors include:
    - INVALID_ARGUMENT: a provided value has failed to semantically validate
    - NOT_FOUND: no schema has been defined

    Args:
        json_body (Apiv1ReadSchemaRequest): ReadSchemaRequest returns the schema from the
            database.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Apiv1ReadSchemaResponse]
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
    json_body: Apiv1ReadSchemaRequest,
) -> Optional[Apiv1ReadSchemaResponse]:
    """Read returns the current Object Definitions for a Permissions System.

     Errors include:
    - INVALID_ARGUMENT: a provided value has failed to semantically validate
    - NOT_FOUND: no schema has been defined

    Args:
        json_body (Apiv1ReadSchemaRequest): ReadSchemaRequest returns the schema from the
            database.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Apiv1ReadSchemaResponse
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: Apiv1ReadSchemaRequest,
) -> Response[Apiv1ReadSchemaResponse]:
    """Read returns the current Object Definitions for a Permissions System.

     Errors include:
    - INVALID_ARGUMENT: a provided value has failed to semantically validate
    - NOT_FOUND: no schema has been defined

    Args:
        json_body (Apiv1ReadSchemaRequest): ReadSchemaRequest returns the schema from the
            database.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Apiv1ReadSchemaResponse]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: Apiv1ReadSchemaRequest,
) -> Optional[Apiv1ReadSchemaResponse]:
    """Read returns the current Object Definitions for a Permissions System.

     Errors include:
    - INVALID_ARGUMENT: a provided value has failed to semantically validate
    - NOT_FOUND: no schema has been defined

    Args:
        json_body (Apiv1ReadSchemaRequest): ReadSchemaRequest returns the schema from the
            database.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Apiv1ReadSchemaResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
