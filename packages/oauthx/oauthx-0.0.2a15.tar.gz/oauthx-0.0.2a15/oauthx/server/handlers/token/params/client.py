# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Annotated
from typing import TypeAlias

import fastapi

from oauthx.lib.exceptions import UnknownClient
from oauthx.lib.protocols import IClient
from oauthx.server.params import Storage
from .assertion import Assertion
from .clientcredentials import ClientCredentials


__all__: list[str] = ['Client']


async def authenticate_client(
    *,
    storage: Storage,
    assertion: Assertion,
    credentials: ClientCredentials,
) -> IClient | None:
    client = None
    if assertion and assertion.is_self_issued():
        raise NotImplementedError
    if credentials and assertion:
        raise NotImplementedError
    if not credentials and not assertion:
        return None

    if credentials and credentials.client_secret:
        client = await storage.get(credentials.client_id)
        if client and not await client.authenticate(credentials.client_secret):
            return None

    if assertion and assertion.is_client():
        client = await storage.get(assertion.client_id)
        if client and not await client.authenticate(assertion.jws):
            return None

    return client


async def get(
    storage: Storage,
    assertion: Assertion,
    credentials: ClientCredentials,
) -> IClient | None:
    client: IClient | None = None
    has_credentials = any([
        credentials and credentials.client_secret,
        assertion
    ])
    if has_credentials:
        client = await authenticate_client(
            storage=storage,
            assertion=assertion,
            credentials=credentials,
        )
    else:
        if credentials is not None:
            client = await storage.get(credentials.client_id)
            if client and client.is_confidential():
                raise UnknownClient(
                    "Client authentication was not successful."
                )

    return client


Client: TypeAlias = Annotated[
    IClient | None,
    fastapi.Depends(get)
]