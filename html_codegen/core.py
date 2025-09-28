"""
Core HTML node classes for creating hierarchical HTML document structures.

This module contains the HTMLNode and HTML classes for building HTML document trees.
HTMLNode represents a tree node, while HTML is an HTML element that inherits from HTMLNode.
The code includes methods for adding nodes, determining parent elements and root,
as well as saving HTML documents to files.

The HTMLNode class also implements a context manager that creates code blocks using the with operator.
When an HTMLNode instance is created inside a with block, it is added to the context stack
of the current execution context. When exiting the with block, all elements of the current context
are added as child elements to the current HTMLNode instance if they don't have a parent element. 
The HTMLNode context manager allows creating hierarchical element structures in HTML documents using with blocks.

The HTML class also allows dynamic creation of child elements through method calls with tag names.
"""
import threading
from collections import defaultdict, namedtuple
from pathlib import Path
from typing import Callable, Optional


def _get_thread_context():
    """Возвращает идентификатор текущего потока."""
    context = [threading.current_thread()]
    return hash(tuple(context))


class HTMLNode:
    """
    HTMLNode - base class for all HTML tree nodes.

    This class provides the fundamental structure for building hierarchical HTML documents.
    It supports context management for clean code organization and thread-safe operations.

    Attributes:
        _parent (Optional[HTMLNode]): Parent node of the current HTML node.
        _nodes (list[HTMLNode]): List of child nodes of the current HTML node.
    """

    frame = namedtuple("frame", ["tag", "items"])
    _with_contexts = defaultdict(list)
    _pending_callbacks = defaultdict(list)  # thread_id -> list of callbacks

    def __init__(self):
        self._parent: Optional[HTMLNode] = None
        self._nodes: list[HTMLNode] = []
        self._ctx = None
        self._created_in_with_context = False
        self._add_to_ctx()

    def __enter__(self) -> "HTMLNode":
        """
        Context manager method for creating HTML nodes.

        Returns:
            HTMLNode: HTML node object.
        """
        stack = HTMLNode._with_contexts[_get_thread_context()]
        stack.append(HTMLNode.frame(self, []))
        return self

    def __exit__(self, *_) -> None:
        thread_id = _get_thread_context()
        stack = HTMLNode._with_contexts[thread_id]
        frame = stack.pop()
        
        # Сначала устанавливаем всех родителей
        for item in frame.items:
            if item.parent:
                continue
            self.add_node(item)
        
        # Затем выполняем все отложенные колбэки
        HTMLNode._execute_pending_callbacks(thread_id)
        
        if not stack:
            del HTMLNode._with_contexts[thread_id]

    @property
    def parent(self) -> Optional["HTMLNode"]:
        """
        Getter method for obtaining the parent node of the current HTML node.

        Returns:
            Optional[HTMLNode]: Parent node of the current HTML node.
        """
        return self._parent

    @parent.setter
    def parent(self, value: "HTMLNode") -> None:
        """
        Setter method for setting the parent node of the current HTML node.

        Args:
            value (HTMLNode): Parent node of the current HTML node.

        Returns:
            None
        """
        self._parent = value
        self.parent_setted_callback()

    def parent_setted_callback(self):
        """
        Callback method called when parent is set.
        
        If the node was created in a with context, the callback is deferred
        until the with block exits. Otherwise, it's executed immediately.
        """
        if self._created_in_with_context:
            # Отложить выполнение колбэка до выхода из with блока
            self._schedule_deferred_callback()
        else:
            # Выполнить колбэк немедленно
            self._execute_parent_callback()
    
    def _schedule_deferred_callback(self):
        """Schedule a deferred callback for execution after with block exits."""
        thread_id = _get_thread_context()
        HTMLNode._pending_callbacks[thread_id].append(self._execute_parent_callback)
    
    def _execute_parent_callback(self):
        """
        Execute the actual parent callback logic.
        
        Override this method in subclasses to implement specific callback behavior.
        """
        pass
    
    @classmethod
    def _execute_pending_callbacks(cls, thread_id: int) -> None:
        """
        Execute all pending callbacks for the given thread.
        
        Args:
            thread_id (int): Thread identifier
        """
        callbacks = cls._pending_callbacks.get(thread_id, [])
        for callback in callbacks:
            try:
                callback()
            except Exception as e:
                # Логируем ошибку, но не прерываем выполнение других колбэков
                print(f"Error executing deferred callback: {e}")
        
        # Очищаем очередь колбэков для этого потока
        cls._pending_callbacks[thread_id].clear()
    
    @staticmethod
    def _get_thread_context():
        """Возвращает идентификатор текущего потока."""
        return _get_thread_context()
    
    def _find_html_tag(self):
        """
        Найти html тег в иерархии родителей или в контексте with блоков.
        
        Returns:
            html: HTML тег или None, если не найден
        """
        from .tags.document_ import html
        
        # Сначала ищем в иерархии родителей
        current = self.parent
        while current:
            if isinstance(current, html):
                return current
            current = current.parent
        
        # Если не нашли в родителях, ищем в контексте with
        thread_id = self._get_thread_context()
        stack = self._with_contexts.get(thread_id, [])
        for frame in stack:
            if isinstance(frame.tag, html):
                return frame.tag
        
        return None

    @property
    def layer(self) -> int:
        """
        Getter method for obtaining the level of the current HTML node.

        Returns:
            int: Level of the current HTML node.
        """
        parent = self.parent
        layer = 0
        while parent:
            if parent is not None:
                layer += 1

            parent = parent.parent

        return layer

    @property
    def root(self) -> "HTMLNode":
        """
        Getter method for obtaining the root node of the current HTML node.

        Returns:
            HTMLNode: Root node of the current HTML node.
        """
        parent = self.parent
        root = self
        while parent:
            if parent is not None:
                root = parent

            parent = parent.parent

        return root

    def add_node_validation(self, new_node: "HTMLNode") -> None:
        """
        Method for validating a child node before adding it to the current HTML node.

        Args:
            new_node (HTMLNode): New child node to validate.

        Returns:
            None
        """
        ...

    def add_node(self, new_node: "HTMLNode") -> None:
        """
        Method for adding a child node to the current HTML node.

        Args:
            new_node (HTMLNode): New child node to add.

        Returns:
            None
        """
        self.add_node_validation(new_node)
        new_node.parent = self
        self._nodes.append(new_node)

    def _add_to_ctx(self) -> None:
        """
        Helper method for adding a node to the current context.

        Returns:
            None
        """
        stack = HTMLNode._with_contexts.get(_get_thread_context())
        if stack:
            self._ctx = stack[-1]
            stack[-1].items.append(self)
            self._created_in_with_context = True


class HTML(HTMLNode):
    """
    HTML - class representing an HTML element.

    This class extends HTMLNode to provide HTML-specific functionality including
    tag names, attributes, and dynamic child element creation.

    Attributes:
        tag_name (str): Tag name of the element
        is_single (bool): Flag indicating whether the element is single (e.g., <img>)
        is_text (bool): Flag indicating whether the element is text
        _attrs (dict): Dictionary of element attributes
        parent (HTML): Parent element
        root (HTML): Root element
        _nodes (list): List of child elements

    """

    def __init__(self, tag_name: str, attrs: Optional[dict] = None):
        """
        Initialize an HTML class instance.

        Args:
            tag_name (str): Tag name of the element
            attrs (dict, optional): Dictionary of element attributes

        """
        super().__init__()
        self.tag_name = tag_name
        self.is_single: bool = False
        self.is_text: bool = False
        self._attrs = attrs or {}

        self.parent: "HTML"
        self.root: "HTML"
        self._nodes: list["HTML"]

    def __repr__(self) -> str:
        """
        Return string representation of the HTML element.

        Returns:
            str: String representation of the HTML element

        """
        from .renderer import Renderer

        return Renderer(self).get_open_tag(self).strip() + Renderer(self).get_close_tag(self).strip()

    def __getattr__(self, tag_name: str) -> Callable:
        """
        Return a function that creates a new HTML element with the specified tag name.
        
        For tags that conflict with Python keywords (input, object, map, del),
        automatically searches for a version with underscore (input_, object_, map_, del_).

        Args:
            tag_name (str): Tag name

        Returns:
            Callable: Function that creates a new HTML element

        """
        from . import tags

        # Список тегов, которые конфликтуют с ключевыми словами Python
        keyword_conflicts = {'input', 'object', 'map', 'del'}
        
        # Если тег конфликтует с ключевым словом, ищем версию с подчеркиванием
        if tag_name in keyword_conflicts:
            tag_class = getattr(tags, f"{tag_name}_", None)
        else:
            tag_class = getattr(tags, tag_name, None)

        def _create_node(*args, **kwargs) -> "HTML":
            if tag_class:
                tag = tag_class(*args, **kwargs)
            else:
                tag = HTML(tag_name, **kwargs)

            self.add_node(tag)
            return tag

        return _create_node

    @property
    def children(self) -> list["HTML"]:
        return self._nodes

    @property
    def in_head(self) -> bool:
        """
        Check if the element is inside a head tag.

        Returns:
            bool: True if the element is inside a head tag, otherwise False

        """
        parent = self.parent
        while parent:
            if parent.tag_name == "head":
                return True

            parent = parent.parent

        return False

    @property
    def in_body(self) -> bool:
        """
        Check if the element is inside a body tag.

        Returns:
            bool: True if the element is inside a body tag, otherwise False

        """
        parent = self.parent
        while parent:
            if parent.tag_name == "body":
                return True

            parent = parent.parent

        return False

    def add_node_validation(self, new_node: "HTML") -> None:
        """
        Check if a new HTML element can be added as a child element.

        Args:
            new_node (HTMLNode): New HTML element

        Raises:
            Exception: If the new element already has a parent

        """
        if new_node.parent:
            raise Exception("node already has parent")

    def save(self, filename: str) -> Path:
        """
        Save the HTML document to a file.

        Args:
            filename (str): File name

        Returns:
            Path: Path object representing the file path

        """
        from .renderer import Renderer

        if not (html_path := Path(filename)).is_absolute():
            html_path = Path(__name__).parent.resolve() / "index.html"

        with open(html_path, "w") as html_file:
            html_file.write(Renderer(self).render())

        return html_path
