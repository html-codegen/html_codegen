"""
Базовые классы и миксины для HTML тегов.
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
        Инициализирует объект текста с заданным текстом.

        Параметры:
            text (str): Текст, который будет установлен для этого узла.
        """
        super().__init__("", {"text": text})
        self.is_text = True

    def add_node_validation(self, new_node: "HTML") -> None:
        raise Exception("Текст не может иметь вложеных тегов")

    def __repr__(self):
        return self._attrs["text"]


class OnlyOneInHTMLTagMixin:
    tag_name: str
    parent: HTML

    def parent_setted_callback(self) -> None:
        from .document_ import html
        if not isinstance(self.parent, html):
            raise Exception(f'Тег "{self.tag_name}" может находиться только внутри тега "html"')

        parent_children = list(map(attrgetter("tag_name"), self.parent.children))
        if self.tag_name in parent_children:
            raise Exception(f'Тег "{self.tag_name}" может быть только один внутри тега "html"')


class OnlyTextTagMixin:
    """
    This mixin class ensures that only text nodes can be added to the tag.

    Attributes:
        tag_name (str): The name of the tag.
    """

    tag_name: str

    def add_node_validation(self, new_node: "HTML") -> None:
        if not new_node.is_text:
            raise Exception(f'Тег "{self.tag_name}" может содержать только текст')


class Tag(HTML):
    """
    This class represents a generic HTML tag. It inherits from the HTML class.
    """

    def __init__(self, attrs: Optional[dict] = None) -> None:
        """
        Инициализирует объект тега с заданными атрибутами.

        Параметры:
            attrs (Optional[dict]): Атрибуты, которые будут установлены для этого тега.
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
        Инициализирует объект одиночного тега с заданными параметрами.

        Параметры:
            *args: Дополнительные позиционные аргументы, которые будут переданы в родительский класс.
            **kwargs: Дополнительные именованные аргументы, которые будут переданы в родительский класс.
        """
        super().__init__(*args, **kwargs)
        self.is_single = True

    def add_node_validation(self, *args) -> None:
        raise Exception(f'Одиночный тег "{self.tag_name}" не может иметь вложеных тегов')
