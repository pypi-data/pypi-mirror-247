from typing import List, Optional, Union, Dict, Tuple

from bhaiapi.models.citation import DraftCitation
from bhaiapi.models.tools.code import CodeContent
from bhaiapi.models.tools.flight import BhaiFlightContent
from bhaiapi.models.tools.gdocs import BhaiGDocsContent
from bhaiapi.models.image import BhaiImageContent
from bhaiapi.models.tools.link import BhaiLink
from bhaiapi.models.tools.map import BhaiMapContent
from bhaiapi.models.tools.tool_declaimer import BhaiToolDeclaimer
from bhaiapi.models.user_content import UserContent
from bhaiapi.models.tools.youtube import BhaiYoutubeContent


class BhaiDraft:
    def __init__(self, input_list: list):
        self._input_list = input_list
        self.id = self._input_list[0]

    @property
    def text(self) -> str:
        return self._input_list[1][0]

    @property
    def citations(self) -> list[DraftCitation]:
        text = self.text
        return (
            [DraftCitation(c, text) for c in self._input_list[2][0]]
            if self._input_list[2]
            else []
        )

    @property
    def images(self) -> list[BhaiImageContent]:
        # also in self._attachments[1]
        return (
            [BhaiImageContent(img) for img in self._input_list[4]]
            if self._input_list[4]
            else []
        )

    @property
    def language(self) -> str:
        # en
        return self._input_list[9]

    @property
    def _attachments(self) -> Optional[list]:
        return self._input_list[12]

    @property
    def map_content(self) -> list[BhaiMapContent]:
        if not self._attachments:
            return []
        return (
            [BhaiMapContent(a) for a in self._attachments[3]]
            if self._attachments[3]
            else []
        )

    @property
    def gdocs(self) -> list[BhaiGDocsContent]:
        if not self._attachments:
            return []
        return (
            [BhaiGDocsContent(a) for a in self._attachments[12][0][2]]
            if self._attachments[12]
            else []
        )

    @property
    def youtube(self) -> list[BhaiYoutubeContent]:
        if not self._attachments:
            return []
        return (
            [BhaiYoutubeContent(a) for a in self._attachments[4]]
            if self._attachments[4]
            else []
        )

    @property
    def python_code(self) -> list[CodeContent]:
        # Google has a dedicated Python model that can also run code.
        # The text model uses the output of the Python model to generate answers,
        # including answers in other languages.
        #
        # The code snippet is the same for all drafts!
        if not self._attachments:
            return []
        return (
            [CodeContent(a) for a in self._attachments[5]]
            if self._attachments[5] and self._attachments[5][0][3]
            else []
        )

    @property
    def links(self) -> list[BhaiLink]:
        if not self._attachments:
            return []
        return (
            [BhaiLink(a) for a in self._attachments[8]] if self._attachments[8] else []
        )

    @property
    def flights(self) -> list[BhaiFlightContent]:
        if not self._attachments:
            return []
        return (
            [BhaiFlightContent(a) for a in self._attachments[16]]
            if self._attachments[16]
            else []
        )

    @property
    def tool_disclaimers(self) -> list[BhaiToolDeclaimer]:
        if not self._attachments or len(self._attachments) < 23:
            return []

        return (
            [BhaiToolDeclaimer(a) for a in self._attachments[22]]
            if self._attachments[22]
            else []
        )

    @property
    def user_content(self) -> Dict[str, UserContent]:
        d = {v.key: v for v in self.youtube}
        d.update({v.key: v for v in self.map_content})
        d.update({v.key: v for v in self.flights})
        d.update({v.key: v for v in self.links})
        d.update({v.key: v for v in self.tool_disclaimers})
        return d

    def __str__(self) -> str:
        return self.text
