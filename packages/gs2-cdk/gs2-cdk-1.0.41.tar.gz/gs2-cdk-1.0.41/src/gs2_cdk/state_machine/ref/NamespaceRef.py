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
from ..stamp_sheet.StartStateMachineByUserId import StartStateMachineByUserId


class NamespaceRef:
    namespace_name: str

    def __init__(
        self,
        namespace_name: str,
    ):
        self.namespace_name = namespace_name

    def start_state_machine(
        self,
        args: Optional[str] = None,
        enable_speculative_execution: Optional[str] = None,
        ttl: Optional[int] = None,
        user_id: Optional[str] = "#{userId}",
    ) -> StartStateMachineByUserId:
        return StartStateMachineByUserId(
            self.namespace_name,
            args,
            enable_speculative_execution,
            ttl,
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
                "stateMachine",
                self.namespace_name,
            ],
        ).str(
        )
