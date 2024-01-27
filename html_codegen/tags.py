from operator import attrgetter
from pathlib import Path
from typing import Optional

from .core import HTML


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

    def add_node_validation(self, *args) -> None:
        raise Exception("Текст не может иметь вложеных тегов")

    def __repr__(self):
        return self._attrs["text"]


class _OnlyOneInHTMLTagMixin:
    tag_name: str
    parent: HTML

    def parent_setted_callback(self) -> None:
        if not isinstance(self.parent, html):
            raise Exception(f'Тег "{self.tag_name}" может находиться только внутри тега "html"')

        parent_children = list(map(attrgetter("tag_name"), self.parent.children))
        if self.tag_name in parent_children:
            raise Exception(f'Тег "{self.tag_name}" может быть только один внутри тега "html"')


class _OnlyTextTagMixin:
    """
    This mixin class ensures that only text nodes can be added to the tag.

    Attributes:
        tag_name (str): The name of the tag.
    """

    tag_name: str

    def add_node_validation(self, new_node: "HTML") -> None:
        if not new_node.is_text:
            raise Exception(f'Тег "{self.tag_name}" может содержать только текст')


class _Tag(HTML):
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


class html(_Tag):
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


class head(_OnlyOneInHTMLTagMixin, _Tag):
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


class body(_OnlyOneInHTMLTagMixin, _Tag):
    """
    This class represents the body section of an HTML document. It inherits from the _Tag class.
    """

    def parent_setted_callback(self):
        super().parent_setted_callback()
        if isinstance(self.root, html) and self.root.use_brython:
            self._attrs["onload"] = "brython()"


class title(_OnlyTextTagMixin, _Tag):
    """
    This class represents a title tag in HTML. It inherits from the _OnlyTextTagMixin and _Tag classes.
    """

    def __init__(self, text: str, /) -> None:
        """
        Инициализирует объект title тега с заданным текстом.

        Параметры:
            text (str): Текст, который будет установлен для этого тега.
        """
        super().__init__()
        self.text(text)


class style(_OnlyTextTagMixin, _Tag):
    """
    This class represents a style tag in HTML. It inherits from the _OnlyTextTagMixin and _Tag classes.
    """

    def __init__(
        self,
        style_path: str,
        *,
        media: Optional[str] = None,
        style_type: Optional[str] = None,
    ) -> None:
        """
        Инициализирует объект style тега с заданным путем к стилю и необязательными медиа и типом стиля.

        Параметры:
            style_path (str): Путь к файлу стиля.
            media (Optional[str]): Медиа, для которых предназначен этот стиль.
            style_type (Optional[str]): Тип этого стиля.
        """
        attrs = {}
        if media:
            attrs["media"] = media
        if style_type:
            attrs["type"] = style_type
        super().__init__(attrs)

        self.text(self._get_code(style_path))

    def _get_code(self, path: str) -> str:
        with open(Path(path), "r") as file:
            return file.read().strip()


class script(_OnlyTextTagMixin, _Tag):
    """
    This class represents a script tag in HTML. It inherits from the _OnlyTextTagMixin and _Tag classes.
    """

    def __init__(self, script_path: Optional[str] = None, **kwargs) -> None:
        """
        Инициализирует объект script тега с заданным путем к скрипту.

        Параметры:
            script_path (Optional[str]): Путь к файлу скрипта.
            **kwargs: Дополнительные именованные аргументы, которые будут переданы в родительский класс.
        """
        super().__init__(kwargs)

        if script_path:
            self.text(self._get_code(script_path))

    def _get_code(self, path: str) -> str:
        with open(Path(path), "r") as file:
            return file.read().strip()


class nav(_Tag):
    """
    This class represents a navigation tag in HTML. It inherits from the _Tag class.
    """


class article(_Tag):
    """
    This class represents an article tag in HTML. It inherits from the _Tag class.
    """


class section(_Tag):
    """
    This class represents a section tag in HTML. It inherits from the _Tag class.
    """


class header(_Tag):
    """
    This class represents a header tag in HTML. It inherits from the _Tag class.
    """


class footer(_Tag):
    """
    This class represents a footer tag in HTML. It inherits from the _Tag class.
    """


class div(_Tag):
    """
    This class represents a div tag in HTML. It inherits from the _Tag class.
    """


class form(_Tag):
    """
    This class represents a form tag in HTML. It inherits from the _Tag class.
    """


class table(_Tag):
    """
    This class represents a table tag in HTML. It inherits from the _Tag class.
    """


class thead(_Tag):
    """
    This class represents a thead tag in HTML. It inherits from the _Tag class.
    """


class tbody(_Tag):
    """
    This class represents a tbody tag in HTML. It inherits from the _Tag class.
    """


class tfoot(_Tag):
    """
    This class represents a tfoot tag in HTML. It inherits from the _Tag class.
    """


class td(_Tag):
    """
    This class represents a td tag in HTML. It inherits from the _Tag class.
    """


class tr(_Tag):
    """
    This class represents a tr tag in HTML. It inherits from the _Tag class.
    """


class th(_Tag):
    """
    This class represents a th tag in HTML. It inherits from the _Tag class.
    """


class ul(_Tag):
    """
    This class represents a ul tag in HTML. It inherits from the _Tag class.
    """


class ol(_Tag):
    """
    This class represents a ol tag in HTML. It inherits from the _Tag class.
    """


class li(_Tag):
    """
    This class represents a li tag in HTML. It inherits from the _Tag class.
    """


class h1(_Tag):
    """
    This class represents a h1 tag in HTML. It inherits from the _Tag class.
    """


class h2(_Tag):
    """
    This class represents a h2 tag in HTML. It inherits from the _Tag class.
    """


class h3(_Tag):
    """
    This class represents a h3 tag in HTML. It inherits from the _Tag class.
    """


class h4(_Tag):
    """
    This class represents a h4 tag in HTML. It inherits from the _Tag class.
    """


class h5(_Tag):
    """
    This class represents a h5 tag in HTML. It inherits from the _Tag class.
    """


class h6(_Tag):
    """
    This class represents a h6 tag in HTML. It inherits from the _Tag class.
    """


class a(_Tag):
    """
    This class represents a a tag in HTML. It inherits from the _Tag class.
    """


class textarea(_Tag):
    """
    This class represents a textarea tag in HTML. It inherits from the _Tag class.
    """


class p(_Tag):
    """
    This class represents a p tag in HTML. It inherits from the _Tag class.
    """


class b(_Tag):
    """
    This class represents a b tag in HTML. It inherits from the _Tag class.
    """


class i(_Tag):
    """
    This class represents a i tag in HTML. It inherits from the _Tag class.
    """


class u(_Tag):
    """
    This class represents a u tag in HTML. It inherits from the _Tag class.
    """


class s(_Tag):
    """
    This class represents a s tag in HTML. It inherits from the _Tag class.
    """


class span(_Tag):
    """
    This class represents a span tag in HTML. It inherits from the _Tag class.
    """


class button(_Tag):
    """
    This class represents a button tag in HTML. It inherits from the _Tag class.
    """


class pyscript(_OnlyTextTagMixin, _Tag):
    """
    This class represents a pyscript tag in HTML. It inherits from the _OnlyTextTagMixin and _Tag classes.
    """

    def __init__(self, module: str, /, **kwargs):
        """
        Инициализирует объект pyscript тега с заданным модулем Python.

        Параметры:
            module (str): Модуль Python, который будет использован в этом теге.
            **kwargs: Дополнительные именованные аргументы, которые будут переданы в родительский класс.
        """
        attrs = kwargs.pop("attrs", {})
        attrs["type"] = "text/python"
        kwargs["attrs"] = attrs
        super(_Tag, self).__init__("script", **kwargs)

        self.text(self._get_module_code(module))

    def parent_setted_callback(self):
        if not isinstance(self.root, html) or not self.root.use_brython:
            raise Exception(
                'Вы не можете использовать "pyscript" тег пока не поставите use_brython=True у "html" тега\n\t'
                "example: `document = html(use_brython=True)`"
            )

    def _get_module_code(self, module_name: str):
        module_path = Path(module_name.replace(".", "/") + ".py")
        with open(module_path, "r") as module_file:
            return module_file.read().strip()


########################################################################################################################
###                                                                                                                  ###
###                                        НЕ ПАРНЫЕ(ОДИНОЧНЫЕ) ТЕГИ                                                 ###
###                                                                                                                  ###
########################################################################################################################


class _SingleTag(_Tag):
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


class link(_SingleTag):
    """
    This class represents a link tag in HTML. It inherits from the _SingleTag class.
    """

    def __init__(self, href: str, /, rel: str, **kwargs) -> None:
        """
        Инициализирует объект link тега с заданными параметрами.

        Параметры:
            href (str): URL, на который должен указывать ссылка.
            rel (str): Отношение между текущим документом и целевым документом.
            **kwargs: Дополнительные именованные аргументы, которые будут переданы в родительский класс.
        """
        attrs = kwargs.get("attrs", {})
        attrs.update({"href": href, "rel": rel})
        kwargs["attrs"] = attrs
        super().__init__(**kwargs)


class hr(_SingleTag):
    """
    This class represents a horizontal rule tag in HTML. It inherits from the _SingleTag class.
    """


class img(_SingleTag):
    """
    This class represents an image tag in HTML. It inherits from the _SingleTag class.
    """


class input(_SingleTag):
    """
    This class represents an input tag in HTML. It inherits from the _SingleTag class.
    """


class meta(_SingleTag):
    """
    This class represents a meta tag in HTML. It inherits from the _SingleTag class.
    """
