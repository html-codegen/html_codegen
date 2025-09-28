"""
Document structure tags (html, head, body).

This module provides the fundamental structural tags that form the backbone
of every HTML document, including the root html tag and its essential
head and body sections.
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
        Initialize an HTML document object with the given parameters.

        Args:
            use_brython (bool): Indicates whether to use Brython in this document.
            **kwargs: Additional arguments that will be passed to the parent class.
        """
        self.use_brython = use_brython
        super().__init__(**kwargs)


class head(OnlyOneInHTMLTagMixin, Tag):
    """
    This class represents the head section of an HTML document. It inherits from the _Tag class.
    """

    def _execute_parent_callback(self):
        """Set up Brython scripts if enabled in the root HTML document."""
        super()._execute_parent_callback()
        if self.root.use_brython:
            self._set_brython()

    def _set_brython(self):
        """Add Brython CDN scripts to the head section."""
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

    def _execute_parent_callback(self):
        """Set up Brython initialization if enabled in the root HTML document."""
        super()._execute_parent_callback()
        if isinstance(self.root, html) and self.root.use_brython:
            self._attrs["onload"] = "brython()"
