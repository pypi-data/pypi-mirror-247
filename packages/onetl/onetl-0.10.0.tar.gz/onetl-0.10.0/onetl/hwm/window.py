#  Copyright 2023 MTS (Mobile Telesystems)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Edge:
    value: Any = None
    including: bool = True

    def is_set(self) -> bool:
        return self.value is not None


@dataclass
class Window:
    expression: str
    start_from: Edge = field(default_factory=Edge)
    stop_at: Edge = field(default_factory=Edge)
