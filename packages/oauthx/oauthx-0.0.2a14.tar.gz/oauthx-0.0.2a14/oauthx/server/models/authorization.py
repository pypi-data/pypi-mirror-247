# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
from typing import Any
from typing import Iterable
from typing import Literal
from typing import MutableMapping
from typing import TypeAlias

import pydantic

from oauthx.lib.protocols import IStorage
from oauthx.server.protocols import IUserInfoContributor
from oauthx.server.types import AuthorizationKey
from .subjectkey import SubjectKey


AuthorizedTokenType: TypeAlias = Literal[
    'urn:ietf:params:oauth:token-type:access_token',
    'urn:ietf:params:oauth:token-type:refresh_token',
    'urn:ietf:params:oauth:token-type:id_token',
]


class Authorization(pydantic.BaseModel):
    """A :class:`Authorization` object represents the authorization granted
    by the resource owner through the authorization endpoint.
    """
    authorized: datetime.datetime = pydantic.Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    client_id: str = pydantic.Field(
        default=...
    )

    id: int = pydantic.Field(
        default=...
    )
    
    issuer: str = pydantic.Field(
        default=...
    )

    lifecycle: Literal['GRANTED', 'ISSUED'] = pydantic.Field(
        default='ISSUED'
    )

    prompted: bool = pydantic.Field(
        default=False
    )

    scope: set[str] = pydantic.Field(
        default_factory=set
    )

    sub: SubjectKey = pydantic.Field(
        default=...
    )
    
    token_types: list[AuthorizedTokenType] = pydantic.Field(
        default=...
    )
    
    userinfo: dict[str, Any] = pydantic.Field(
        default={}
    )

    @property
    def pk(self) -> AuthorizationKey:
        return AuthorizationKey(self.id)

    def allows_scope(self, scope: Iterable[str]) -> bool:
        return set(scope) <= self.scope

    def is_consumed(self) -> bool:
        return self.lifecycle == 'ISSUED'

    def contribute(self, contributor: IUserInfoContributor) -> None:
        contributor.contribute_to_userinfo(self.userinfo)

    def contribute_to_userinfo(self, userinfo: MutableMapping[str, Any]) -> None:
        userinfo.update(self.userinfo)

    def grants_id_token(self) -> bool:
        return 'urn:ietf:params:oauth:token-type:id_token' in self.token_types

    async def consume(self, storage: IStorage) -> None:
        self.lifecycle = 'ISSUED'
        await storage.persist(self)