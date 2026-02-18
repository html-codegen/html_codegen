from .base_ import OnlyOneInHTMLTagMixin, Tag


class html(Tag):

    def __init__(self, *, use_brython: bool = False, **kwargs) -> None:
        self.use_brython = use_brython
        super().__init__(**kwargs)


class head(OnlyOneInHTMLTagMixin, Tag):

    def _execute_parent_callback(self) -> None:
        super()._execute_parent_callback()
        if self.root.use_brython:
            self._set_brython()

    def _set_brython(self) -> None:
        brython_cdn = [
            "https://cdn.jsdelivr.net/npm/brython@3/brython.min.js",
            "https://cdn.jsdelivr.net/npm/brython@3/brython_stdlib.js",
        ]
        for brython_path in brython_cdn:
            self.script(type="text/javascript", src=brython_path)


class body(OnlyOneInHTMLTagMixin, Tag):

    def _execute_parent_callback(self) -> None:
        super()._execute_parent_callback()
        if isinstance(self.root, html) and self.root.use_brython:
            self._attrs["onload"] = "brython()"
