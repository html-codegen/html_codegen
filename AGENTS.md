# Инструкции для агентов

**Commit:** 0305e51 | **Branch:** main

---

## Обзор проекта

**html_codegen** — Python библиотека для программной генерации HTML документов с поддержкой Brython (клиентский Python в браузере).

- **Python**: 3.12+
- **Менеджер пакетов**: uv
- **Репозиторий**: GitLab (html_codegen/html_codegen)

---

## Команды сборки, линтинга и тестов

### Установка и запуск

```bash
# Установка зависимостей
uv sync

# Запуск примера
uv run main.py

# Активация виртуального окружения (опционально)
source .venv/bin/activate
```

### Линтинг и форматирование

```bash
# Ruff (линтер + автофикс)
uv run ruff check . --fix

# Black (форматирование)
uv run black .

# isort (сортировка импортов)
uv run isort .

# Запуск всех проверок через pre-commit
uv run pre-commit run --all-files
```

### Документация (Sphinx)

```bash
# Сборка документации
uv run sphinx-build -b html docs/source docs/build

# Локальный просмотр документации
open docs/build/index.html
```

### Тесты

```bash
# Запуск тестов (через Makefile, если настроен)
make tests

# Или напрямую pytest (если добавлен)
uv run pytest
uv run pytest tests/test_specific.py -v          # Конкретный файл
uv run pytest tests/test_specific.py::test_name  # Конкретный тест
```

---

## Структура проекта

```
html_codegen/
├── html_codegen/           # Основной пакет библиотеки
│   ├── __init__.py         # Экспорты и документация модуля
│   ├── core.py             # Базовые классы: HTMLNode, HTML
│   ├── renderer.py         # Класс Renderer для генерации HTML
│   └── tags/               # HTML теги, организованные по категориям
│       ├── __init__.py     # Экспорт всех тегов
│       ├── base_.py        # Базовые классы: Tag, SingleTag, text, миксины
│       ├── document_.py    # Структурные теги: html, head, body
│       ├── text_.py        # Текстовые теги: h1-h6, p, span, code и др.
│       ├── semantic_.py    # Семантические теги: article, section, nav
│       ├── forms_.py       # Формы: form, input, button, select
│       ├── media_.py       # Медиа: img, video, audio, canvas
│       ├── tables_.py      # Таблицы: table, tr, td, th
│       ├── lists_.py       # Списки: ul, ol, li, dl
│       ├── metadata_.py    # Метаданные: meta, link, style, script
│       └── interactive_.py # Интерактивные: a, div, hr
├── main.py                 # Пример использования библиотеки
├── web/                    # Веб-ассеты для примеров
│   ├── styles/             # CSS файлы
│   └── scripts/py/         # Python скрипты для Brython
├── docs/                   # Sphinx документация
│   ├── source/             # RST исходники
│   └── build/              # Собранная документация
└── pyproject.toml          # Конфигурация проекта
```

---

## WHERE TO LOOK

| Task | Location |
|------|----------|
| Публичное API | `html_codegen/tags/__init__.py` — экспорт 70+ тегов |
| Базовые классы | `html_codegen/core.py` — HTMLNode, HTML |
| Рендеринг | `html_codegen/renderer.py` — класс Renderer |
| Пример использования | `main.py` |
| Теги (подробно) | `html_codegen/tags/AGENTS.md` |

---

## Стиль кода

### Общие правила

- **Длина строки**: 120 символов
- **Кодировка**: UTF-8
- **Отступы**: 4 пробела
- **Кавычки**: двойные `"` для строк (предпочтительно)

### Импорты (isort)

Порядок импортов (настройка в `.isort.cfg`):

```python
# 1. Стандартная библиотека
import threading
from collections import defaultdict, namedtuple
from pathlib import Path
from typing import Callable, Optional

# 2. Сторонние библиотеки (если есть)

# 3. Локальные импорты (FIRSTPARTY)
from .core import HTML
from . import tags
```

Правила:
- `profile = black` — совместимость с black
- `multi_line_output = 3` (Vertical Hanging Indent)
- `include_trailing_comma = True`
- `force_grid_wrap = 2`
- `use_parentheses = True`

### Именование

- **Классы**: `PascalCase` (пример: `HTMLNode`, `SingleTag`, `OnlyOneInHTMLTagMixin`)
- **Функции/методы**: `snake_case` (пример: `add_node`, `get_inner_html`)
- **Приватные методы**: `_leading_underscore` (пример: `_add_to_ctx`, `_execute_parent_callback`)
- **Константы**: `UPPER_SNAKE_CASE`
- **Атрибуты класса**: `_leading_underscore` для внутренних (пример: `_parent`, `_nodes`, `_attrs`)
- **Теги, конфликтующие с ключевыми словами Python**: добавляется `_` в конец (пример: `input_`, `object_`, `map_`, `del_`)

### Типизация

Используйте type hints везде:

```python
from typing import Optional, Callable

def __init__(self, tag_name: str, attrs: Optional[dict] = None) -> None:
    self._parent: Optional[HTMLNode] = None
    self._nodes: list[HTMLNode] = []

def __getattr__(self, tag_name: str) -> Callable:
    ...

@property
def children(self) -> list["HTML"]:
    return self._nodes
```

### Документирование (Google Style Docstrings)

```python
def add_node(self, new_node: "HTMLNode") -> None:
    """
    Method for adding a child node to the current HTML node.

    Args:
        new_node (HTMLNode): New child node to add.

    Returns:
        None
    """
    ...
```

- Модули: описание в начале файла (тройные кавычки)
- Классы: описание класса с Attributes
- Методы/функции: Args, Returns, Raises (если применимо)

### Обработка ошибок

Использовать исключения с понятными сообщениями:

```python
def add_node_validation(self, new_node: "HTML") -> None:
    if new_node.parent:
        raise Exception("node already has parent")

def add_node_validation(self, new_node: "HTML") -> None:
    if not new_node.is_text:
        raise Exception(f'Tag "{self.tag_name}" can only contain text')
```

---

## Архитектурные паттерны

### Наследование тегов

Все HTML теги наследуются от базовых классов:

```python
# Простой тег
class div(Tag):
    pass

# Одиночный тег (без закрывающего тега)
class img(SingleTag):
    pass

# Тег с ограничениями (только один в документе)
class head(OnlyOneInHTMLTagMixin, Tag):
    pass

# Текстовый узел
class text(HTML):
    pass
```

### Context Manager

Библиотека поддерживает `with` блоки для построения иерархии:

```python
with html() as doc:
    with head():
        title("My Page")
    with body():
        div().p().text("Hello")
```

### Динамическое создание тегов

Через `__getattr__` на HTML элементах:

```python
body = html_document.body()
body.div(attrs={"id": "container"})
body.div().button().text("Click")
```

---

## Анти-паттерны (запрещённые действия)

### Архитектура тегов
- **НЕ** добавляйте дочерние узлы в `text` — текстовые узлы не могут содержать вложенности
- **НЕ** добавляйте дочерние узлы в `SingleTag` (img, br, hr и др.)
- **НЕ** размещайте `head`, `body` вне тега `html`
- **НЕ** создавайте несколько `head` или `body` в одном документе

### Структура DOM
- **НЕ** добавляйте узел, у которого уже есть родитель

### Brython
- **НЕ** используйте `pyscript` без `html(use_brython=True)`

---

## Важные замечания

- **Не коммитьте** без явного запроса пользователя
- **Не подавляйте** type errors через `# type: ignore` или `as any`
- **Следуйте** существующим паттернам в кодовой базе
- **Проверяйте** линтером изменённые файлы (`ruff check <file>`)
