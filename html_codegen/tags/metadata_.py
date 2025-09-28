"""
Metadata tags.

This module provides HTML tags for document metadata and head section elements,
including title, meta, link, style, and script tags.
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
        Initialize a title tag object with the given text.

        Args:
            text_content (str): Text that will be set for this tag.
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
        Initialize a link tag object with the given parameters.

        Args:
            href (str): URL that the link should point to.
            rel (str): Relationship between the current document and the target document.
            **kwargs: Additional keyword arguments that will be passed to the parent class.
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
        Initialize a style tag object with the given style path and optional media and style type.

        Args:
            style_path (str): Path to the style file.
            media (Optional[str]): Media for which this style is intended.
            style_type (Optional[str]): Type of this style.
        """
        attrs = {}
        if media:
            attrs["media"] = media
        if style_type:
            attrs["type"] = style_type
        super().__init__(attrs)

        from .base_ import text
        self.add_node(text(self._get_code(style_path)))

    def _get_code(self, path: str) -> str:
        """Read and return the contents of a file."""
        with open(Path(path), "r") as file:
            return file.read().strip()


class script(OnlyTextTagMixin, Tag):
    """
    This class represents a script tag in HTML. It inherits from the _OnlyTextTagMixin and _Tag classes.
    """

    def __init__(self, script_path: Optional[str] = None, **kwargs) -> None:
        """
        Initialize a script tag object with the given script path.

        Args:
            script_path (Optional[str]): Path to the script file.
            **kwargs: Additional keyword arguments that will be passed to the parent class.
        """
        super().__init__(kwargs)

        if script_path:
            self.text(self._get_code(script_path))

    def _get_code(self, path: str) -> str:
        """Read and return the contents of a file."""
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
        Initialize a pyscript tag object with the given Python module.

        Args:
            module (str): Python module that will be used in this tag.
            **kwargs: Additional keyword arguments that will be passed to the parent class.
        """
        attrs = kwargs.pop("attrs", {})
        attrs["type"] = "text/python"
        kwargs["attrs"] = attrs
        super(Tag, self).__init__("script", **kwargs)

        self.text(self._get_module_code(module))

    def _execute_parent_callback(self):
        """Validate that Brython is enabled for pyscript tags."""
        html_tag = self._find_html_tag()
        
        if not html_tag or not html_tag.use_brython:
            raise Exception(
                'You cannot use "pyscript" tag until you set use_brython=True for "html" tag\n\t'
                "example: `document = html(use_brython=True)`"
            )

    def _get_module_code(self, module_name: str):
        """Read and return the contents of a Python module file."""
        try:
            module_path = Path(module_name.replace(".", "/") + ".py")
            with open(module_path, "r") as module_file:
                return module_file.read().strip()
        except FileNotFoundError:
            # If file doesn't exist, return a placeholder
            return f"# Module {module_name} not found"
