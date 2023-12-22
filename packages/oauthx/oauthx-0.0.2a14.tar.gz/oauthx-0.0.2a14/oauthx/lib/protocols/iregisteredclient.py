# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import MutableMapping
from typing import Protocol


class IRegisteredClient(Protocol):
    __module__: str = 'oauthx.lib.protocols'

    @property
    def id(self) -> str:
        ...

    def contribute_to_event(self, data: MutableMapping[str, Any]) -> None: ...
    def get_display_name(self) -> str: ...