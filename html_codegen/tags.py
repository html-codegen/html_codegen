from pathlib import Path
from typing import Optional

from .core import HTML
 

class text(HTML):
    def __init__(self, text: str, /) -> None:
        super().__init__('', {'text': text})
        self.is_text = True
        
    def add_node_validation(self, *args) -> None:
        raise Exception('Текст не может иметь вложеных тегов')

    def __repr__(self):
        return self._attrs["text"]


class _Tag(HTML):
    def __init__(self, attrs: Optional[dict] = None) -> None:
        super().__init__(self.__class__.__name__, attrs)


class html(_Tag):
    def __init__(self, *, use_brython: bool = False, **kwargs):
        self.use_brython = use_brython
        super().__init__(**kwargs)


class head(_Tag):
    def parent_setted_callback(self):
        if isinstance(self.root, html) and self.root.use_brython:
            self._set_brython()

    def _set_brython(self):
        brython_cdn = [
            "https://cdn.jsdelivr.net/npm/brython@3/brython.min.js",
            "https://cdn.jsdelivr.net/npm/brython@3/brython_stdlib.js",
        ]
        for brython_path in brython_cdn:
            self.script(attrs={'type': 'text/javascript', 'src': brython_path})


class body(_Tag):
    def parent_setted_callback(self):
        if isinstance(self.root, html) and self.root.use_brython:
            self._attrs['onload'] = 'brython()'


class title(_Tag):
    def __init__(self, text: str, /) -> None:
        super().__init__()
        self.text(text)


class style(_Tag):
    def __init__(self, style_path: str, *, media: Optional[str] = None, style_type: Optional[str] = None) -> None:
        attrs = {}
        if media:
            attrs['media'] = media
        if style_type:
            attrs['type'] = style_type
        super().__init__(attrs)

        self.text(self._get_style_code(style_path))

    def _get_style_code(self, style_path: str) -> str:
        with open(Path(style_path), 'r') as style_file:
            return style_file.read().strip()


class pyscript(_Tag):
    def __init__(self, module: str, /, **kwargs):
        attrs = kwargs.get('attrs', {})
        attrs['type'] = 'text/python'
        kwargs['attrs'] = attrs
        super(_Tag, self).__init__('script', **kwargs)

        self.text(self._get_module_code(module))

    def parent_setted_callback(self):
        if not isinstance(self.root, html) or not self.root.use_brython:
            raise Exception(
                'Вы не можете использовать "pyscript" тег пока не поставите use_brython=True у "html" тега\n\t'
                'example: `document = html(use_brython=True)`'

            )

    def _get_module_code(self, module_name: str):
        module_path = Path(module_name.replace('.', '/') + '.py')
        with open(module_path, 'r') as module_file:
            return module_file.read().strip()


########################################################################################################################
###                                                                                                                  ###
###                                        НЕ ПАРНЫЕ(ОДИНОЧНЫЕ) ТЕГИ                                                 ###
###                                                                                                                  ###
########################################################################################################################

class _SingleTag(_Tag):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.is_single = True
        
    def add_node_validation(self, *args) -> None:
        raise Exception('Одиночный тег не может иметь вложеных тегов')


class link(_SingleTag):
    def __init__(self, href: str, /, rel: str, **kwargs) -> None:
        attrs = kwargs.get('attrs', {})
        attrs.update({'href': href, 'rel': rel})
        kwargs['attrs'] = attrs
        super().__init__(**kwargs)


class hr(_SingleTag):
    pass


class img(_SingleTag):
    pass


class input(_SingleTag):
    pass


class meta(_SingleTag):
    pass
