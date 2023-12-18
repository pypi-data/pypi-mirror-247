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
from .options.RateModelOptions import RateModelOptions
from .options.RateModelTimingTypeIsImmediateOptions import RateModelTimingTypeIsImmediateOptions
from .options.RateModelTimingTypeIsAwaitOptions import RateModelTimingTypeIsAwaitOptions
from .enum.RateModelTimingType import RateModelTimingType


class RateModel:
    name: str
    timing_type: RateModelTimingType
    metadata: Optional[str] = None
    consume_actions: Optional[List[ConsumeAction]] = None
    lock_time: Optional[int] = None
    enable_skip: Optional[bool] = None
    skip_consume_actions: Optional[List[ConsumeAction]] = None
    acquire_actions: Optional[List[AcquireAction]] = None

    def __init__(
        self,
        name: str,
        timing_type: RateModelTimingType,
        options: Optional[RateModelOptions] = RateModelOptions(),
    ):
        self.name = name
        self.timing_type = timing_type
        self.metadata = options.metadata if options.metadata else None
        self.consume_actions = options.consume_actions if options.consume_actions else None
        self.lock_time = options.lock_time if options.lock_time else None
        self.enable_skip = options.enable_skip if options.enable_skip else None
        self.skip_consume_actions = options.skip_consume_actions if options.skip_consume_actions else None
        self.acquire_actions = options.acquire_actions if options.acquire_actions else None

    @staticmethod
    def timing_type_is_immediate(
        name: str,
        options: Optional[RateModelTimingTypeIsImmediateOptions] = RateModelTimingTypeIsImmediateOptions(),
    ) -> RateModel:
        return RateModel(
            name,
            RateModelTimingType.IMMEDIATE,
            RateModelOptions(
                options.metadata,
                options.consume_actions,
                options.skip_consume_actions,
                options.acquire_actions,
            ),
        )

    @staticmethod
    def timing_type_is_await(
        name: str,
        lock_time: int,
        enable_skip: bool,
        options: Optional[RateModelTimingTypeIsAwaitOptions] = RateModelTimingTypeIsAwaitOptions(),
    ) -> RateModel:
        return RateModel(
            name,
            RateModelTimingType.AWAIT,
            RateModelOptions(
                lock_time,
                enable_skip,
                options.metadata,
                options.consume_actions,
                options.skip_consume_actions,
                options.acquire_actions,
            ),
        )

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
        if self.timing_type is not None:
            properties["timingType"] = self.timing_type.value
        if self.lock_time is not None:
            properties["lockTime"] = self.lock_time
        if self.enable_skip is not None:
            properties["enableSkip"] = self.enable_skip
        if self.skip_consume_actions is not None:
            properties["skipConsumeActions"] = [
                v.properties(
                )
                for v in self.skip_consume_actions
            ]
        if self.acquire_actions is not None:
            properties["acquireActions"] = [
                v.properties(
                )
                for v in self.acquire_actions
            ]

        return properties
