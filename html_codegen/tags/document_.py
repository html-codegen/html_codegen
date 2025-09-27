"""
Структурные теги документа (html, head, body).
"""
from .base_ import OnlyOneInHTMLTagMixin, Tag


class html(Tag):
    """
    This class represents an HTML document. It inherits from the _Tag class.

    Attributes:
        use_brython (bool): Indicates whether Brython should be used in this document.
    """

    def __init__(self, *, use_brython: bool = False, **kwargs):
        """
        Инициализирует объект HTML документа с заданными параметрами.

        Параметры:
            use_brython (bool): Указывает, следует ли использовать Brython в этом документе.
            **kwargs: Дополнительные аргументы, которые будут переданы в родительский класс.
        """
        self.use_brython = use_brython
        super().__init__(**kwargs)


class head(OnlyOneInHTMLTagMixin, Tag):
    """
    This class represents the head section of an HTML document. It inherits from the _Tag class.
    """

    def parent_setted_callback(self):
        super().parent_setted_callback()
        if self.root.use_brython:
            self._set_brython()

    def _set_brython(self):
        brython_cdn = [
            "https://cdn.jsdelivr.net/npm/brython@3/brython.min.js",
            "https://cdn.jsdelivr.net/npm/brython@3/brython_stdlib.js",
        ]
        for brython_path in brython_cdn:
            self.script(type="text/javascript", src=brython_path)


class body(OnlyOneInHTMLTagMixin, Tag):
    """
    This class represents the body section of an HTML document. It inherits from the _Tag class.
    """

    def parent_setted_callback(self):
        super().parent_setted_callback()
        if isinstance(self.root, html) and self.root.use_brython:
            self._attrs["onload"] = "brython()"
