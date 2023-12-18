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
from .SalesItem import SalesItem
from .SalesItemGroup import SalesItemGroup
from .DisplayItem import DisplayItem
from .options.ShowcaseOptions import ShowcaseOptions


class Showcase:
    name: str
    display_items: List[DisplayItem]
    metadata: Optional[str] = None
    sales_period_event_id: Optional[str] = None

    def __init__(
        self,
        name: str,
        display_items: List[DisplayItem],
        options: Optional[ShowcaseOptions] = ShowcaseOptions(),
    ):
        self.name = name
        self.display_items = display_items
        self.metadata = options.metadata if options.metadata else None
        self.sales_period_event_id = options.sales_period_event_id if options.sales_period_event_id else None

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.name is not None:
            properties["name"] = self.name
        if self.metadata is not None:
            properties["metadata"] = self.metadata
        if self.sales_period_event_id is not None:
            properties["salesPeriodEventId"] = self.sales_period_event_id
        if self.display_items is not None:
            properties["displayItems"] = [
                v.properties(
                )
                for v in self.display_items
            ]

        return properties
