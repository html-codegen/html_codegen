from operator import attrgetter
from typing import Optional

from ..core import HTML
from ..exceptions import (
    DuplicateTagError,
    OnlyTextContentError,
    SingleTagNestingError,
    TagOutsideHtmlError,
    TextNodeNestingError,
)


class text(HTML):

    def __init__(self, text: str, /) -> None:
        super().__init__("", {"text": text})
        self.is_text = True

    def add_node_validation(self, new_node: "HTML") -> None:
        raise TextNodeNestingError("Text cannot have nested tags")

    def __repr__(self) -> str:
        return self._attrs["text"]


class OnlyOneInHTMLTagMixin:
    tag_name: str
    parent: HTML

    def _execute_parent_callback(self) -> None:
        html_tag = self._find_html_tag()
        
        if not html_tag:
            raise TagOutsideHtmlError(f'Tag "{self.tag_name}" can only be placed inside an "html" tag')

        html_children = list(map(attrgetter("tag_name"), html_tag.children))
        if html_children.count(self.tag_name) > 1:
            raise DuplicateTagError(f'Tag "{self.tag_name}" can only appear once inside an "html" tag')


class OnlyTextTagMixin:
    tag_name: str

    def add_node_validation(self, new_node: "HTML") -> None:
        if not new_node.is_text:
            raise OnlyTextContentError(f'Tag "{self.tag_name}" can only contain text')


class Tag(HTML):

    def __init__(self, attrs: Optional[dict] = None) -> None:
        super().__init__(self.__class__.__name__, attrs)


class SingleTag(Tag):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.is_single = True

    def add_node_validation(self, *args) -> None:
        raise SingleTagNestingError(f'Single tag "{self.tag_name}" cannot have nested tags')
