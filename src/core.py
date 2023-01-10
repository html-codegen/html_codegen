from collections import defaultdict, namedtuple
import importlib
import threading
from typing import Callable, Optional


SINGLE_TAGS = [
    'br',
    'hr',
    'img',
    'input',
    'meta',
    'link',
]


def _get_thread_context():
  context = [threading.current_thread()]
  return hash(tuple(context))


class HTMLNode:
    frame = namedtuple('frame', ['tag', 'items'])
    _with_contexts = defaultdict(list)

    def __init__(self):
        self._parent: Optional[HTMLNode] = None
        self._nodes: list[HTMLNode] = []
        self._ctx = None
        self._add_to_ctx()

    def __enter__(self) -> 'HTMLNode':
        stack = HTMLNode._with_contexts[_get_thread_context()]
        stack.append(HTMLNode.frame(self, []))
        return self

    def __exit__(self, *_) -> None:
        thread_id = _get_thread_context()
        stack = HTMLNode._with_contexts[thread_id]
        frame = stack.pop()
        for item in frame.items:
            if item.parent: continue
            self.add_node(item)
        if not stack:
            del HTMLNode._with_contexts[thread_id]

    @property
    def parent(self) -> Optional['HTMLNode']:
        return self._parent

    @parent.setter
    def parent(self, value: 'HTMLNode') -> None:
        self._parent = value

    @property
    def layer(self) -> int:
        parent = self.parent
        layer = 0
        while parent:
            if parent is not None:
                layer += 1

            parent = parent.parent

        return layer

    @property
    def root(self) -> 'HTMLNode':
        parent = self.parent
        root = self
        while parent:
            if parent is not None:
                root = parent

            parent = parent.parent

        return root

    def add_node_validation(self, new_node: 'HTMLNode') -> None:
        return

    def add_node(self, new_node: 'HTMLNode') -> None:
        self.add_node_validation(new_node)
        new_node.parent = self
        self._nodes.append(new_node)

    def _add_to_ctx(self) -> None:
        stack = HTMLNode._with_contexts.get(_get_thread_context())
        if stack:
            self._ctx = stack[-1]
            stack[-1].items.append(self)


class HTML(HTMLNode):
    def __init__(self, tag_name: str = 'html', /, attrs: Optional[dict] = None):
        super().__init__()
        self.tag_name = tag_name
        self.is_single: bool = tag_name in SINGLE_TAGS
        self.is_text: bool = tag_name == 'text'
        self._attrs = attrs or {}

        self.parent: 'HTML'

    def __repr__(self) -> str:
        from src.renderer import Renderer
        return Renderer(self).get_open_tag(self).strip() + Renderer(self).get_close_tag(self).strip()

    def __getattr__(self, tag_name: str) -> Callable:
        def _get_tag_class():
            module = importlib.import_module('.tags', package='src')
            return getattr(module, tag_name)

        def _create_node(*args, attrs: Optional[dict] = None) -> 'HTML':
            if tag_class := _get_tag_class():
                tag = tag_class(*args, attrs=attrs)
            else:
                tag = HTML(tag_name, attrs)

            self.add_node(tag)
            return tag

        return _create_node

    def add_node_validation(self, new_node: 'HTML') -> None:
        if self.is_single or self.is_text:
            raise Exception

        if new_node.parent:
            raise Exception('node already has parent')

    @property
    def in_head(self) -> bool:
        parent = self.parent
        while parent:
            if parent.tag_name == "head":
                return True

            parent = parent.parent

        return False

    @property
    def in_body(self) -> bool:
        parent = self.parent
        while parent:
            if parent.tag_name == "body":
                return True

            parent = parent.parent

        return False
