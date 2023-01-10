from typing import Optional
from pathlib import Path

from .core import HTML


class _Tag(HTML):
    def __init__(self, attrs: Optional[dict] = None):
        super().__init__(self.__class__.__name__, attrs)


class _SingleTag(_Tag):
    def add_node_validation(self, *args) -> None:
        raise Exception("Одиночный тег не может иметь вложеных тегов")


class text(_Tag):
    def add_node_validation(self, *args) -> None:
        raise Exception("Текст не может иметь вложеных тегов")


class hr(_SingleTag):
    pass


class style(_SingleTag):
    pass


class img(_SingleTag):
    pass


class input(_SingleTag):
    pass


class meta(_SingleTag):
    pass


class link(_SingleTag):
    pass


class label(_Tag):
    pass


class title(_Tag):
    pass


class body(_Tag):
    pass


class head(_Tag):
    pass


class div(_Tag):
    pass


class p(_Tag):
    pass


class b(_Tag):
    pass


class h1(_Tag):
    pass


class h2(_Tag):
    pass


class h3(_Tag):
    pass


class h4(_Tag):
    pass


class h5(_Tag):
    pass


class h6(_Tag):
    pass


class button(_Tag):
    pass


class script(_Tag):
    pass


class pyscript(_Tag):
    def __init__(self, module: str, attrs: Optional[dict] = None):
        attrs = attrs or {}
        attrs['type'] = 'text/python'
        super(_Tag, self).__init__('script', attrs)

        self.text(attrs={'text': self._get_module_code(module)})

    def _get_module_code(self, module_name: str):
        module_path = Path(module_name.replace('.', '/') + '.py')
        with open(module_path, 'r') as module_file:
            return module_file.read().strip()


if __name__ == "__main__":
    assert div().tag_name == 'div'
    assert p().tag_name == 'p'
    assert b().tag_name == 'b'
    assert h1().tag_name == 'h1'
