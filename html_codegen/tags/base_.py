"""
Base classes and mixins for HTML tags.

This module provides the fundamental building blocks for all HTML tags,
including base classes, mixins, and utility classes that define common
behavior and validation rules.
"""
from operator import attrgetter
from typing import Optional

from ..core import HTML


class text(HTML):
    """
    This class represents a text node in HTML. It inherits from the HTML class.

    Attributes:
        is_text (bool): Indicates whether this node is a text node.
    """

    def __init__(self, text: str, /) -> None:
        """
        Initialize a text object with the given text.

        Args:
            text (str): Text that will be set for this node.
        """
        super().__init__("", {"text": text})
        self.is_text = True

    def add_node_validation(self, new_node: "HTML") -> None:
        raise Exception("Text cannot have nested tags")

    def __repr__(self):
        return self._attrs["text"]


class OnlyOneInHTMLTagMixin:
    """
    Mixin class that ensures a tag can only appear once within an HTML document.
    
    This mixin validates that the tag is placed inside an HTML tag and that
    no other instance of the same tag already exists in the document.
    """
    tag_name: str
    parent: HTML

    def _execute_parent_callback(self) -> None:
        """Validate that the tag is properly placed within an HTML document."""
        html_tag = self._find_html_tag()
        
        if not html_tag:
            raise Exception(f'Tag "{self.tag_name}" can only be placed inside an "html" tag')

        # Проверяем уникальность только среди прямых детей html тега
        html_children = list(map(attrgetter("tag_name"), html_tag.children))
        if html_children.count(self.tag_name) > 1:
            raise Exception(f'Tag "{self.tag_name}" can only appear once inside an "html" tag')


class OnlyTextTagMixin:
    """
    This mixin class ensures that only text nodes can be added to the tag.

    Attributes:
        tag_name (str): The name of the tag.
    """

    tag_name: str

    def add_node_validation(self, new_node: "HTML") -> None:
        if not new_node.is_text:
            raise Exception(f'Tag "{self.tag_name}" can only contain text')


class Tag(HTML):
    """
    This class represents a generic HTML tag. It inherits from the HTML class.
    """

    def __init__(self, attrs: Optional[dict] = None) -> None:
        """
        Initialize a tag object with the given attributes.

        Args:
            attrs (Optional[dict]): Attributes that will be set for this tag.
        """
        super().__init__(self.__class__.__name__, attrs)


class SingleTag(Tag):
    """
    This class represents a single tag in HTML. It inherits from the _Tag class.

    Attributes:
        is_single (bool): Indicates whether this tag is a single tag.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize a single tag object with the given parameters.

        Args:
            *args: Additional positional arguments that will be passed to the parent class.
            **kwargs: Additional keyword arguments that will be passed to the parent class.
        """
        super().__init__(*args, **kwargs)
        self.is_single = True

    def add_node_validation(self, *args) -> None:
        raise Exception(f'Single tag "{self.tag_name}" cannot have nested tags')
