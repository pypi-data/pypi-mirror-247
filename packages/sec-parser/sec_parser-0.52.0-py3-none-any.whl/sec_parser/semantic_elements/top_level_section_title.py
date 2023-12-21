from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sec_parser.semantic_elements.abstract_semantic_element import (
    AbstractLevelElement,
    AbstractSemanticElement,
)
from sec_parser.semantic_elements.mixins.dict_text_content_mixin import (
    DictTextContentMixin,
)

if TYPE_CHECKING:  # pragma: no cover
    from sec_parser.processing_engine.html_tag import HtmlTag
    from sec_parser.processing_engine.processing_log import LogItemOrigin, ProcessingLog
    from sec_parser.semantic_elements.top_level_section_title_types import (
        TopLevelSectionType,
    )


class TopLevelSectionTitle(DictTextContentMixin, AbstractLevelElement):
    """
    The TopLevelSectionTitle class represents the title and the beginning of a top-level
    section of a document. For instance, in SEC 10-Q reports, a
    top-level section could be "Part I, Item 3. Quantitative and Qualitative
    Disclosures About Market Risk.".
    """

    def __init__(
        self,
        html_tag: HtmlTag,
        *,
        processing_log: ProcessingLog | None = None,
        log_origin: LogItemOrigin | None = None,
        level: int | None = None,
        section_type: TopLevelSectionType | None = None,
    ) -> None:
        super().__init__(
            html_tag,
            processing_log=processing_log,
            level=level,
            log_origin=None,
        )
        if section_type is None:
            msg = "section_type cannot be None"
            raise ValueError(msg)
        self.section_type = section_type
        self.log_init(log_origin)

    @classmethod
    def create_from_element(
        cls,
        source: AbstractSemanticElement,
        log_origin: LogItemOrigin,
        *,
        level: int | None = None,
        section_type: TopLevelSectionType | None = None,
    ) -> AbstractLevelElement:
        return cls(
            source._html_tag,  # noqa: SLF001
            level=level,
            section_type=section_type,
            processing_log=source.processing_log,
            log_origin=log_origin,
        )

    def to_dict(
        self,
        *,
        include_previews: bool = False,
        include_contents: bool = False,
    ) -> dict[str, Any]:
        return {
            **super().to_dict(
                include_previews=include_previews,
                include_contents=include_contents,
            ),
            "section_type": self.section_type.identifier,
        }
