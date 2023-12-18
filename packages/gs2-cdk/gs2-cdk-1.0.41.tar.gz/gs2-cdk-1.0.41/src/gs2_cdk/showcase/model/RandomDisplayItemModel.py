# Copyright 2016- Game Server Services, Inc. or its affiliates. All Rights
# Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
from __future__ import annotations
from typing import *
from ...core.model import ConsumeAction
from ...core.model import AcquireAction
from .options.RandomDisplayItemModelOptions import RandomDisplayItemModelOptions


class RandomDisplayItemModel:
    name: str
    acquire_actions: List[AcquireAction]
    stock: int
    weight: int
    metadata: Optional[str] = None
    consume_actions: Optional[List[ConsumeAction]] = None

    def __init__(
        self,
        name: str,
        acquire_actions: List[AcquireAction],
        stock: int,
        weight: int,
        options: Optional[RandomDisplayItemModelOptions] = RandomDisplayItemModelOptions(),
    ):
        self.name = name
        self.acquire_actions = acquire_actions
        self.stock = stock
        self.weight = weight
        self.metadata = options.metadata if options.metadata else None
        self.consume_actions = options.consume_actions if options.consume_actions else None

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.name is not None:
            properties["name"] = self.name
        if self.metadata is not None:
            properties["metadata"] = self.metadata
        if self.consume_actions is not None:
            properties["consumeActions"] = [
                v.properties(
                )
                for v in self.consume_actions
            ]
        if self.acquire_actions is not None:
            properties["acquireActions"] = [
                v.properties(
                )
                for v in self.acquire_actions
            ]
        if self.stock is not None:
            properties["stock"] = self.stock
        if self.weight is not None:
            properties["weight"] = self.weight

        return properties
