"""Define a base client for interacting with Notion."""
from __future__ import annotations

from typing import Any, cast

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError
from pydantic import ValidationError

from aionotion.bridge import Bridge
from aionotion.const import LOGGER
from aionotion.device import Device
from aionotion.errors import InvalidCredentialsError, RequestError
from aionotion.helpers.model import NotionBaseModel, NotionBaseModelT
from aionotion.sensor import Sensor
from aionotion.system import System
from aionotion.user import User

API_BASE: str = "https://api.getnotion.com/api"

DEFAULT_TIMEOUT: int = 10


class Client:  # pylint: disable=too-few-public-methods
    """Define the API object."""

    def __init__(self, *, session: ClientSession | None = None) -> None:
        """Initialize.

        Args:
            session: An optional aiohttp ClientSession.
        """
        self._session = session
        self._token: str | None = None
        self.user_uuid: str = ""

        self.bridge = Bridge(self)
        self.device = Device(self)
        self.sensor = Sensor(self)
        self.system = System(self)
        self.user = User(self)

    async def async_authenticate(self, email: str, password: str) -> None:
        """Authenticate the user and retrieve an authentication token.

        Args:
            email: The email address of a Notion account.
            password: The account password.
        """
        auth_response = await self.async_request(
            "post",
            "users/sign_in",
            json={"sessions": {"email": email, "password": password}},
        )

        self._token = auth_response["session"]["authentication_token"]
        self.user_uuid = auth_response["session"]["user_id"]

    async def async_request(
        self, method: str, endpoint: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        """Make an API request.

        Args:
            method: An HTTP method.
            endpoint: A relative API endpoint.
            **kwargs: Additional kwargs to send with the request.

        Returns:
            An API response payload.

        Raises:
            InvalidCredentialsError: Raised upon invalid credentials.
            RequestError: Raised upon an underlying HTTP error.
        """
        url: str = f"{API_BASE}/{endpoint}"

        kwargs.setdefault("headers", {})
        if self._token:
            kwargs["headers"]["Authorization"] = f"Token token={self._token}"

        if use_running_session := self._session and not self._session.closed:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        data: dict[str, Any] = {}

        async with session.request(method, url, **kwargs) as resp:
            data = await resp.json()

            try:
                resp.raise_for_status()
            except ClientError as err:
                if "401" in str(err):
                    raise InvalidCredentialsError("Invalid credentials") from err
                raise RequestError(data["errors"][0]["title"]) from err

        if not use_running_session:
            await session.close()

        LOGGER.debug("Received data from /%s: %s", endpoint, data)

        return data

    async def async_request_and_validate(
        self,
        method: str,
        endpoint: str,
        model: type[NotionBaseModel],
        **kwargs: dict[str, Any],
    ) -> NotionBaseModelT:
        """Make an API request and validate the response against a Pydantic model.

        Args:
            method: An HTTP method.
            endpoint: A relative API endpoint.
            model: A Pydantic model to validate the response against.
            **kwargs: Additional kwargs to send with the request.

        Returns:
            A parsed, validated Pydantic model representing the response.
        """
        raw_data = await self.async_request(method, endpoint, **kwargs)

        try:
            return cast(NotionBaseModelT, model.model_validate(raw_data))
        except ValidationError as err:
            raise RequestError(
                f"Error while parsing response from {endpoint}: {err}"
            ) from err


async def async_get_client(
    email: str, password: str, *, session: ClientSession | None = None
) -> Client:
    """Return an authenticated API object.

    Args:
        email: The email address of a Notion account.
        password: The account password.
        session: An optional aiohttp ClientSession.

    Returns:
        An authenticated Client object.
    """
    client = Client(session=session)
    await client.async_authenticate(email, password)
    return client
