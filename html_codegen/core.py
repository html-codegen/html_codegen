"""
Этот модуль содержит классы HTMLNode и HTML для создания иерархии узлов HTML-документа.
Класс HTMLNode представляет узел дерева, а HTML - элемент HTML-документа, наследуемый от HTMLNode.
В коде есть методы для добавления узлов, определения родительского элемента и корня,
а также сохранения HTML-документа в файл.

Класс HTMLNode также реализует контекстный менеджер, который создает блоки кода с помощью оператора with.
Когда создается экземпляр HTMLNode внутри блока with, он добавляется в стек контекста текущего потока выполнения.
При выходе из блока with все элементы текущего контекста удаляются из стека
и добавляются как дочерние элементы к текущему экземпляру HTMLNode, если у них нет родительского элемента.
Контекстный менеджер HTMLNode позволяет создавать иерархическую структуру элементов
в HTML-документе с помощью блоков with.

Класс HTML также позволяет динамически создавать дочерние элементы с помощью вызовов методов с названиями тегов.
"""
from collections import defaultdict, namedtuple
from pathlib import Path
import threading
from typing import Callable, Optional


def _get_thread_context():
    """Возвращает идентификатор текущего потока."""
    context = [threading.current_thread()]
    return hash(tuple(context))


class HTMLNode:
    """
    HTMLNode - базовый класс для всех узлов HTML-дерева.

    Attributes:
        _parent (Optional[HTMLNode]): Родительский узел текущего узла HTML.
        _nodes (list[HTMLNode]): Список дочерних узлов текущего узла HTML.
        _ctx: Контекст текущего узла.
    """

    frame = namedtuple('frame', ['tag', 'items'])
    _with_contexts = defaultdict(list)

    def __init__(self):
        self._parent: Optional[HTMLNode] = None
        self._nodes: list[HTMLNode] = []
        self._ctx = None
        self._add_to_ctx()

    def __enter__(self) -> 'HTMLNode':
        """
        Метод-контекстный менеджер для создания узла HTML.
        
        Returns:
            HTMLNode: Объект HTML-узла.
        """
        stack = HTMLNode._with_contexts[_get_thread_context()]
        stack.append(HTMLNode.frame(self, []))
        return self

    def __exit__(self, *_) -> None:
        """
        Метод, который вызывается при выходе из контекста создания узла.
        
        Args:
            _: Возвращает ничего.
        """
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
        """
        Getter-метод для получения родительского узла текущего узла HTML.
        
        Returns:
            Optional[HTMLNode]: Родительский узел текущего узла HTML.
        """
        return self._parent

    @parent.setter
    def parent(self, value: 'HTMLNode') -> None:
        """
        Setter-метод для установки родительского узла текущего узла HTML.
        
        Args:
            value (HTMLNode): Родительский узел текущего узла HTML.
        
        Returns:
            None
        """
        self._parent = value

        self.parent_setted_callback()

    def parent_setted_callback(self):
        ...

    @property
    def layer(self) -> int:
        """
        Getter-метод для получения уровня текущего узла HTML.
        
        Returns:
            int: Уровень текущего узла HTML.
        """
        parent = self.parent
        layer = 0
        while parent:
            if parent is not None:
                layer += 1

            parent = parent.parent

        return layer

    @property
    def root(self) -> 'HTMLNode':
        """
        Getter-метод для получения корневого узла текущего узла HTML.
        
        Returns:
            HTMLNode: Корневой узел текущего узла HTML.
        """
        parent = self.parent
        root = self
        while parent:
            if parent is not None:
                root = parent

            parent = parent.parent

        return root

    def add_node_validation(self, new_node: 'HTMLNode') -> None:
        """
        Метод для проверки дочернего узла перед добавлением в текущий узел HTML.
        
        Args:
            new_node (HTMLNode): Новый дочерний узел, который нужно проверить.
        
        Returns:
            None
        """
        ...

    def add_node(self, new_node: 'HTMLNode') -> None:
        """
        Метод для добавления дочернего узла в текущий узел HTML.
        
        Args:
            new_node (HTMLNode): Новый дочерний узел, который нужно добавить.
        
        Returns:
            None
        """
        self.add_node_validation(new_node)
        new_node.parent = self
        self._nodes.append(new_node)

    def _add_to_ctx(self) -> None:
        """
        Вспомогательный метод для добавления узла в контекст текущего узла HTML.
        
        Returns:
            None
        """
        stack = HTMLNode._with_contexts.get(_get_thread_context())
        if stack:
            self._ctx = stack[-1]
            stack[-1].items.append(self)


class HTML(HTMLNode):
    """
    HTML - класс, представляющий HTML-элемент.

    Attributes:
        tag_name (str): имя тега элемента
        is_single (bool): флаг, указывающий, является ли элемент одиночным (например, <img>)
        is_text (bool): флаг, указывающий, является ли элемент текстовым
        _attrs (dict): словарь атрибутов элемента
        parent (HTML): родительский элемент
        root (HTML): корневой элемент
        _nodes (list): список дочерних элементов

    """
    def __init__(self, tag_name: str, attrs: Optional[dict] = None):
        """
        Инициализирует экземпляр класса HTML.

        Args:
            tag_name (str): имя тега элемента
            attrs (dict, optional): словарь атрибутов элемента

        """
        super().__init__()
        self.tag_name = tag_name
        self.is_single: bool = False
        self.is_text: bool = False
        self._attrs = attrs or {}

        self.parent: 'HTML'
        self.root: 'HTML'
        self._nodes: list['HTML']

    def __repr__(self) -> str:
        """
        Возвращает строковое представление HTML-элемента.

        Returns:
            str: строковое представление HTML-элемента

        """
        from .renderer import Renderer
        return Renderer(self).get_open_tag(self).strip() + Renderer(self).get_close_tag(self).strip()

    def __getattr__(self, tag_name: str) -> Callable:
        """
        Возвращает функцию, которая создает новый HTML-элемент с указанным именем тега.

        Args:
            tag_name (str): имя тега

        Returns:
            Callable: функция, создающая новый HTML-элемент

        """
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
        """
        Проверяет, находится ли элемент внутри тега head.

        Returns:
            bool: True, если элемент находится внутри тега head, иначе False

        """
        parent = self.parent
        while parent:
            if parent.tag_name == 'head':
                return True

            parent = parent.parent

        return False

    @property
    def in_body(self) -> bool:
        """
        Проверяет, находится ли элемент внутри тега body.

        Returns:
            bool: True, если элемент находится внутри тега body, иначе False

        """
        parent = self.parent
        while parent:
            if parent.tag_name == 'body':
                return True

            parent = parent.parent

        return False

    def add_node_validation(self, new_node: 'HTML') -> None:
        """
        Проверяет, может ли новый HTML-элемент быть добавлен как дочерний элемент.

        Args:
            new_node (HTMLNode): новый HTML-элемент

        Raises:
            Exception: если у нового элемента уже есть родитель

        """
        if new_node.parent:
            raise Exception('node already has parent')

    def save(self, filename: str) -> Path:
        """
        Сохраняет HTML-документ в файл.

        Args:
            filename (str): имя файла

        Returns:
            Path: объект класса Path, представляющий путь к файлу

        """
        from .renderer import Renderer

        if not (html_path := Path(filename)).is_absolute():
            html_path = Path(__name__).parent.resolve() / 'index.html'

        with open(html_path, 'w') as html_file:
            html_file.write(Renderer(self).render())

        return html_path
