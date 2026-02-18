# HTML Tags Module

**Package:** `html_codegen.tags` — HTML теги, организованные по категориям.

---

## WHERE TO LOOK

| Task | File | Notes |
|------|------|-------|
| Добавить новый тег | `base_.py` или по категории | Наследуй от Tag/SingleTag |
| Изменить экспорт | `__init__.py` | Добавь в `__all__` |
| Базовые классы | `base_.py` | Tag, SingleTag, text, миксины |
| Структурные (html, head, body) | `document_.py` | Только один в документе |
| Текстовые (h1-p, span, code) | `text_.py` | Заголовки, параграфы |
| Семантические (article, nav) | `semantic_.py` | HTML5 семантика |
| Формы (form, input, button) | `forms_.py` | input_, textarea |
| Медиа (img, video, canvas) | `media_.py` | object_, map_, area |
| Таблицы (table, tr, td) | `tables_.py` | Полная структура |
| Списки (ul, ol, li) | `lists_.py` | dl, dt, dd, menu |
| Метаданные (meta, link, script) | `metadata_.py` | title, style, pyscript |
| Интерактивные (a, div, hr) | `interactive_.py` | data |

---

## Паттерны наследования

```python
# Простой тег с атрибутами
class div(Tag):
    pass

# Одиночный тег (без </tag>)
class img(SingleTag):
    pass

# Тег только с текстом (title, style, script)
class title(OnlyTextTagMixin, Tag):
    pass

# Тег в единственном экземпляре (head, body)
class head(OnlyOneInHTMLTagMixin, Tag):
    pass
```

---

## Добавление нового тега

1. Определи класс в соответствующем файле категории
2. Наследуй от правильного базового класса
3. Добавь импорт и экспорт в `__init__.py`
4. Для конфликтов с keywords — добавь `_` в конец

```python
# Пример: новый тег <custom>
# В interactive_.py:
class custom(Tag):
    pass

# В __init__.py:
from .interactive_ import custom
__all__ = [..., "custom"]
```

---

## Миксины

| Миксин | Ограничение | Примеры |
|--------|-------------|---------|
| `OnlyOneInHTMLTagMixin` | Только один в html | head, body |
| `OnlyTextTagMixin` | Только текст внутри | title, style, script |

---

## Теги с суффиксом `_` (конфликт с keywords)

| Тег | Имя класса | Причина |
|-----|------------|---------|
| `<input>` | `input_` | keyword input |
| `<del>` | `del_` | keyword del |
| `<object>` | `object_` | keyword object |
| `<map>` | `map_` | builtin map |

---

## Специальные теги

### `pyscript` (Brython)
- Требует `html(use_brython=True)`
- Путь к модулю: `body.pyscript("web.scripts.py.hello")`

### `text`
- Не наследует от Tag, а от HTML напрямую
- Не может содержать дочерние элементы
