from collections import defaultdict, namedtuple
from pathlib import Path
import threading
from typing import Callable, Optional


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

        self.parent_setted_callback()

    def parent_setted_callback(self):
        ...

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
        ...

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
    def __init__(self, tag_name: str, attrs: Optional[dict] = None):
        super().__init__()
        self.tag_name = tag_name
        self.is_single: bool = False
        self.is_text: bool = False
        self._attrs = attrs or {}

        self.parent: 'HTML'
        self.root: 'HTML'
        self._nodes: list['HTML']

    def __repr__(self) -> str:
        from .renderer import Renderer
        return Renderer(self).get_open_tag(self).strip() + Renderer(self).get_close_tag(self).strip()

    def __getattr__(self, tag_name: str) -> Callable:
        def _get_tag_class() -> Optional[type['HTML']]:
            from . import tags
            return getattr(tags, tag_name, None)

        def _create_node(*args, **kwargs) -> 'HTML':
            if tag_class := _get_tag_class():
                tag = tag_class(*args,  **kwargs)
            else:
                tag = HTML(tag_name, **kwargs)

            self.add_node(tag)
            return tag

        return _create_node

    @property
    def in_head(self) -> bool:
        parent = self.parent
        while parent:
            if parent.tag_name == 'head':
                return True

            parent = parent.parent

        return False

    @property
    def in_body(self) -> bool:
        parent = self.parent
        while parent:
            if parent.tag_name == 'body':
                return True

            parent = parent.parent

        return False

    def add_node_validation(self, new_node: 'HTML') -> None:
        if new_node.parent:
            raise Exception('node already has parent')

    def save(self, filename: str) -> Path:
        from .renderer import Renderer

        if not (html_path := Path(filename)).is_absolute():
            html_path = Path(__name__).parent.resolve() / 'index.html'

        with open(html_path, 'w') as html_file:
            html_file.write(Renderer(self).render())

        return html_path
