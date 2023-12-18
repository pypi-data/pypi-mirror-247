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

from ...core.func import GetAttr, Join
from ..stamp_sheet.IncreaseCounterByUserId import IncreaseCounterByUserId
from ..stamp_sheet.DecreaseCounterByUserId import DecreaseCounterByUserId


class CounterModelRef:
    namespace_name: str
    counter_name: str

    def __init__(
        self,
        namespace_name: str,
        counter_name: str,
    ):
        self.namespace_name = namespace_name
        self.counter_name = counter_name

    def increase_counter(
        self,
        value: int,
        user_id: Optional[str] = "#{userId}",
    ) -> IncreaseCounterByUserId:
        return IncreaseCounterByUserId(
            self.namespace_name,
            self.counter_name,
            value,
            user_id,
        )

    def decrease_counter(
        self,
        value: int,
        user_id: Optional[str] = "#{userId}",
    ) -> DecreaseCounterByUserId:
        return DecreaseCounterByUserId(
            self.namespace_name,
            self.counter_name,
            value,
            user_id,
        )

    def grn(
        self,
    ) -> str:
        return Join(
            ":",
            [
                "grn",
                "gs2",
                GetAttr.region(
                ).str(
                ),
                GetAttr.owner_id(
                ).str(
                ),
                "mission",
                self.namespace_name,
                "counter",
                self.counter_name,
            ],
        ).str(
        )
