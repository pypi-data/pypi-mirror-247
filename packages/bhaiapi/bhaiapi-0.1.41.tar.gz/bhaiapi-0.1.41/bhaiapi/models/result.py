from typing import List, Optional, Union, Dict, Tuple

from bhaiapi.models.draft import BhaiDraft
from bhaiapi.models.tools.tool import BhaiTool


class BhaiUserLocation:
    def __init__(self, input_list: list):
        self._input_list = input_list

    @property
    def location_str(self) -> str:
        return self._input_list[0]

    @property
    def description(self) -> str:
        return self._input_list[1]

    @property
    def geo_position(self) -> list:
        return self._input_list[3][0][0][3]

    @property
    def image_url(self) -> str:
        return "https:" + self._input_list[4]

    def __str__(self) -> str:
        return self.location_str


class BhaiResult:
    def __init__(self, input_list: list):
        self._input_list = input_list
        self.conversation_id = self._input_list[1][0]
        self.response_id = self._input_list[1][1]

    @property
    def search_queries(self) -> list[str, int]:
        return self._input_list[2]

    @property
    def factuality_queries(self) -> Optional[list]:
        return self._input_list[3]

    @property
    def drafts(self) -> list[BhaiDraft]:
        return (
            [BhaiDraft(c) for c in self._input_list[4]] if self._input_list[4] else []
        )

    @property
    def location(self) -> BhaiUserLocation:
        return BhaiUserLocation(self._input_list[5])

    @property
    def progress_tool(self) -> BhaiTool:
        return BhaiTool(self._input_list[6]) if self._input_list[6] else None

    @property
    def country(self) -> str:
        return self._input_list[8]

    @property
    def topic(self) -> Optional[str]:
        if len(self._input_list) < 11 or not self._input_list[10]:
            return None
        return self._input_list[10][0]

    @property
    def tools_applied(self) -> list[BhaiTool]:
        if len(self._input_list) < 12:
            return []
        return (
            [BhaiTool(tool) for tool in self._input_list[11]]
            if self._input_list[11]
            else []
        )
