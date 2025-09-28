"""
HTML tags organized by logical modules.

This module provides a comprehensive collection of HTML5 tags organized into
logical categories for easy import and use. All tags are implemented as classes
that inherit from base tag classes and provide proper HTML semantics.

Categories:
- Base classes and mixins
- Document structure tags
- Semantic HTML5 tags
- Text formatting tags
- List tags
- Table tags
- Form tags
- Media tags
- Metadata tags
- Interactive elements
"""

# Базовые классы и миксины
from .base_ import text, OnlyOneInHTMLTagMixin, OnlyTextTagMixin, Tag, SingleTag

# Структурные теги документа
from .document_ import html, head, body

# Семантические теги
from .semantic_ import (
    main,
    nav,
    article,
    section,
    header,
    footer,
    aside,
    figure,
    figcaption,
    details,
    summary,
    dialog,
    mark,
    time,
    progress,
    meter,
)

# Текстовые теги и форматирование
from .text_ import (
    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    p,
    b,
    strong,
    i,
    em,
    u,
    s,
    del_,
    ins,
    small,
    sub,
    sup,
    code,
    pre,
    kbd,
    samp,
    var,
    cite,
    q,
    blockquote,
    address,
    span,
    br,
    wbr,
)

# Теги списков
from .lists_ import ul, ol, li, dl, dt, dd, menu, menuitem

# Теги таблиц
from .tables_ import (
    table,
    caption,
    colgroup,
    col,
    thead,
    tbody,
    tfoot,
    tr,
    th,
    td,
)

# Теги форм
from .forms_ import (
    form,
    fieldset,
    legend,
    label,
    input_,
    textarea,
    button,
    select,
    option,
    optgroup,
    datalist,
)

# Медиа теги
from .media_ import (
    img,
    audio,
    video,
    source,
    track,
    iframe,
    embed,
    object_,
    param,
    canvas,
    svg,
    map_,
    area,
)

# Метаданные теги
from .metadata_ import title, meta, link, base, style, script, noscript, pyscript

# Интерактивные элементы
from .interactive_ import a, hr, div, data

# Экспорт всех тегов для обратной совместимости
__all__ = [
    # Базовые классы
    "text",
    "OnlyOneInHTMLTagMixin",
    "OnlyTextTagMixin",
    "Tag",
    "SingleTag",
    # Структурные теги
    "html",
    "head",
    "body",
    # Семантические теги
    "main",
    "nav",
    "article",
    "section",
    "header",
    "footer",
    "aside",
    "figure",
    "figcaption",
    "details",
    "summary",
    "dialog",
    "mark",
    "time",
    "progress",
    "meter",
    # Текстовые теги
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "b",
    "strong",
    "i",
    "em",
    "u",
    "s",
    "del_",
    "ins",
    "small",
    "sub",
    "sup",
    "code",
    "pre",
    "kbd",
    "samp",
    "var",
    "cite",
    "q",
    "blockquote",
    "address",
    "span",
    "br",
    "wbr",
    # Теги списков
    "ul",
    "ol",
    "li",
    "dl",
    "dt",
    "dd",
    "menu",
    "menuitem",
    # Теги таблиц
    "table",
    "caption",
    "colgroup",
    "col",
    "thead",
    "tbody",
    "tfoot",
    "tr",
    "th",
    "td",
    # Теги форм
    "form",
    "fieldset",
    "legend",
    "label",
    "input_",
    "textarea",
    "button",
    "select",
    "option",
    "optgroup",
    "datalist",
    # Медиа теги
    "img",
    "audio",
    "video",
    "source",
    "track",
    "iframe",
    "embed",
    "object_",
    "param",
    "canvas",
    "svg",
    "map_",
    "area",
    # Метаданные теги
    "title",
    "meta",
    "link",
    "base",
    "style",
    "script",
    "noscript",
    "pyscript",
    # Интерактивные элементы
    "a",
    "hr",
    "div",
    "data",
]
