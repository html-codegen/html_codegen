"""
Метаданные теги.
"""
from pathlib import Path
from typing import Optional

from .base_ import OnlyTextTagMixin, SingleTag, Tag


class title(OnlyTextTagMixin, Tag):
    """
    This class represents a title tag in HTML. It inherits from the _OnlyTextTagMixin and _Tag classes.
    """

    def __init__(self, text_content: str, /) -> None:
        """
        Инициализирует объект title тега с заданным текстом.

        Параметры:
            text_content (str): Текст, который будет установлен для этого тега.
        """
        super().__init__()
        from .base_ import text
        self.add_node(text(text_content))


class meta(SingleTag):
    """
    This class represents a meta tag in HTML. It inherits from the _SingleTag class.
    """


class link(SingleTag):
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


class base(SingleTag):
    """
    This class represents a base tag in HTML. It inherits from the _SingleTag class.
    """


class style(OnlyTextTagMixin, Tag):
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


class script(OnlyTextTagMixin, Tag):
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


class noscript(Tag):
    """
    This class represents a noscript tag in HTML. It inherits from the _Tag class.
    """


class pyscript(OnlyTextTagMixin, Tag):
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
        super(Tag, self).__init__("script", **kwargs)

        self.text(self._get_module_code(module))

    def parent_setted_callback(self):
        from .document_ import html
        if not isinstance(self.root, html) or not self.root.use_brython:
            raise Exception(
                'Вы не можете использовать "pyscript" тег пока не поставите use_brython=True у "html" тега\n\t'
                "example: `document = html(use_brython=True)`"
            )

    def _get_module_code(self, module_name: str):
        module_path = Path(module_name.replace(".", "/") + ".py")
        with open(module_path, "r") as module_file:
            return module_file.read().strip()
