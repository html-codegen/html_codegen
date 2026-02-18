from pathlib import Path
from typing import Optional

from .base_ import OnlyTextTagMixin, SingleTag, Tag
from ..exceptions import BrythonNotEnabledError


def _read_file_content(path: str) -> str:
    with open(Path(path), "r") as file:
        return file.read().strip()


class title(OnlyTextTagMixin, Tag):

    def __init__(self, text_content: str, /) -> None:
        super().__init__()
        from .base_ import text
        self.add_node(text(text_content))


class meta(SingleTag):
    pass


class link(SingleTag):

    def __init__(self, href: str, /, rel: str, **kwargs) -> None:
        attrs = kwargs.get("attrs", {})
        attrs.update({"href": href, "rel": rel})
        kwargs["attrs"] = attrs
        super().__init__(**kwargs)


class base(SingleTag):
    pass


class style(OnlyTextTagMixin, Tag):

    def __init__(
        self,
        style_path: str,
        *,
        media: Optional[str] = None,
        style_type: Optional[str] = None,
    ) -> None:
        attrs = {}
        if media:
            attrs["media"] = media
        if style_type:
            attrs["type"] = style_type
        super().__init__(attrs)

        from .base_ import text
        self.add_node(text(_read_file_content(style_path)))


class script(OnlyTextTagMixin, Tag):

    def __init__(self, script_path: Optional[str] = None, **kwargs) -> None:
        super().__init__(kwargs)

        if script_path:
            self.text(_read_file_content(script_path))


class noscript(Tag):
    pass


class pyscript(OnlyTextTagMixin, Tag):

    def __init__(self, module: str, /, **kwargs) -> None:
        attrs = kwargs.pop("attrs", {})
        attrs["type"] = "text/python"
        kwargs["attrs"] = attrs
        super().__init__(**kwargs)
        self.tag_name = "script"
        self.text(self._get_module_code(module))

    def _execute_parent_callback(self) -> None:
        html_tag = self._find_html_tag()
        
        if not html_tag or not html_tag.use_brython:
            raise BrythonNotEnabledError(
                'You cannot use "pyscript" tag until you set use_brython=True for "html" tag\n\t'
                "example: `document = html(use_brython=True)`"
            )

    def _get_module_code(self, module_name: str) -> str:
        try:
            module_path = Path(module_name.replace(".", "/") + ".py")
            return _read_file_content(str(module_path))
        except FileNotFoundError:
            return f"# Module {module_name} not found"
