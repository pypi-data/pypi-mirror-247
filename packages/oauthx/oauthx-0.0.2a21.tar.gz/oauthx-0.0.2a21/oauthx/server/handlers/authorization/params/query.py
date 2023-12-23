# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi
from typing import Any

from oauthx.lib.types import RequestURI
from oauthx.lib.types import ResponseType

__all__: list[str] = [
    'CLIENT_ID',
    'REDIRECT_URI',
    'REQUEST',
    'REQUEST_URI',
    'RESPONSE_TYPE',
    'SCOPE',
    'STATE'
]

CLIENT_ID: str = fastapi.Query(
    default=...,
    title="Client ID",
    description="Identifies the client that is requesting an access token."
)

PROMPT: Any = fastapi.Query(
    default=None,
    title="Prompt",
    description=(
        "Space delimited, case sensitive list of ASCII string values that "
        "specifies whether the Authorization Server prompts the End-User "
        "for reauthentication and consent."
    )
)

REDIRECT_URI: str | None = fastapi.Query(
    default=None,
    title="Redirect URI",
    description=(
        "The client redirection endpoint. This URI **must** be priorly "
        "whitelisted for the client specified by `client_id`. If the "
        "client has multiple allowed redirect URIs and did not "
        "configure a default, then this parameter is **required**."
    )
)

REQUEST: str | None = fastapi.Query(
    default=None,
    alias='request',
    title="Request",
    description=(
        "A JSON Web Token (JWT) whose JWT Claims Set holds the "
        "JSON-encoded OAuth 2.0 authorization request parameters. "
        "Must not be used in combination with the `request_uri` "
        "parameter, and all other parameters except `client_id` "
        "must be absent.\n\n"
        "Confidential and credentialed clients must first sign "
        "the claims using their private key, and then encrypt the "
        "result with the public keys that are provided by the "
        "authorization server through the `jwks_uri` specified "
        "in its metadata."
    )
)

REQUEST_URI: RequestURI | None = fastapi.Query(
    default=None,
    title="Request URI",
    description=(
        "References a Pushed Authorization Request (PAR) or a remote "
        "object containing the authorization request.\n\n"
        "If the authorization request was pushed to this authorization "
        "server, then the format of the `request_uri` parameter is "
        "`urn:ietf:params:oauth:request_uri:<reference-value>`. "
        "Otherwise, it is an URI using the `https` scheme. If the "
        "`request_uri` parameter is a remote object, then the external "
        "domain must have been priorly whitelisted by the client."
    )
)

RESPONSE_MODE: str | None = fastapi.Query(
    default=None,
    title="Response mode",
    description=(
        "Informs the Authorization Server of the mechanism to be used "
        "for returning Authorization Response parameters from the "
        "Authorization Endpoint. This use of this parameter is "
        "**not recommended with a value that specifies the same "
        "Response Mode as the default Response Mode for the "
        "Response Type used."
    )
)

RESPONSE_TYPE: ResponseType | None = fastapi.Query(
    default=None,
    title="Response type",
    description="Specifies the response type.",
)

SCOPE: Any | None = fastapi.Query(
    default=None,
    title="Scope",
    description=(
        "The space-delimited scope that is requested by the client."
    )
)

STATE: str | None = fastapi.Query(
    default=None,
    alias='state',
    title="State",
    description=(
        "An opaque value used by the client to maintain state between the "
        "request and callback.  The authorization server includes this "
        "value when redirecting the user-agent back to the client."
    )
)