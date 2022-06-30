from collections import defaultdict, namedtuple
import threading
from typing import Callable, Optional

from renderer import Renderer


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


class HTML:
    frame = namedtuple('frame', ['tag', 'items'])
    _with_contexts = defaultdict(list)

    def __init__(self, tag_name: str = 'html', /, **attrs):
        self.tag_name = tag_name
        self.is_single: bool = tag_name in SINGLE_TAGS
        self.is_text: bool = tag_name == 'text'

        self._parent: Optional[HTML] = None
        self._nodes: list[HTML] = []
        self._attrs: dict = attrs

        self._ctx = None
        self._add_to_ctx()

    def __repr__(self) -> str:
        return Renderer.get_open_tag(self) + Renderer.get_close_tag(self)

    def __enter__(self) -> 'HTML':
        stack = HTML._with_contexts[_get_thread_context()]
        stack.append(HTML.frame(self, []))
        return self

    def __exit__(self, *_) -> None:
        thread_id = _get_thread_context()
        stack = HTML._with_contexts[thread_id]
        frame = stack.pop()
        for item in frame.items:
            if item.parent: continue
            self.add_node(item)
        if not stack:
            del HTML._with_contexts[thread_id]

    def __getattr__(self, tag_name) -> Callable[..., 'HTML']:
        return lambda **attrs: self.create_node(tag_name, **attrs)

    @property
    def parent(self) -> Optional['HTML']:
        return self._parent

    @parent.setter
    def parent(self, value: 'HTML') -> None:
        self._parent = value

    @property
    def root(self) -> 'HTML':
        parent = self.parent
        root = self
        while parent:
            if parent is not None:
                root = parent

            parent = parent.parent

        return root

    def create_node(self, tag_name: str, **attrs) -> 'HTML':
        if self.is_single or self.is_text:
            raise Exception
        new_node = HTML(tag_name, **attrs)
        return self.add_node(new_node)

    def add_node(self, node: 'HTML') -> 'HTML':
        if self.is_single or self.is_text:
            raise Exception
        if node.parent:
            raise Exception('node already has parent')
        node.parent = self
        self._nodes.append(node)
        return node

    def _add_to_ctx(self) -> None:
        stack = HTML._with_contexts.get(_get_thread_context())
        if stack:
            self._ctx = stack[-1]
            stack[-1].items.append(self)
