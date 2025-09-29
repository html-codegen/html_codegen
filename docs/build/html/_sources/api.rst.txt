API Reference
=============

Этот раздел содержит полную документацию по API библиотеки HTML Codegen.

Основные модули
---------------

Модули библиотеки HTML Codegen:

* :mod:`html_codegen.core` - Основные классы для работы с HTML узлами
* :mod:`html_codegen.renderer` - Классы для рендеринга HTML документов  
* :mod:`html_codegen.tags` - Коллекция HTML тегов по категориям

Модуль core
-----------

Основные классы для работы с HTML узлами и документами.

.. automodule:: html_codegen.core
   :members:
   :undoc-members:
   :show-inheritance:

Модуль renderer
---------------

Классы для рендеринга HTML документов.

.. automodule:: html_codegen.renderer
   :members:
   :undoc-members:
   :show-inheritance:

Модуль tags
-----------

Коллекция HTML тегов, организованных по категориям.

.. automodule:: html_codegen.tags
   :members:
   :undoc-members:
   :show-inheritance:

Базовые теги
~~~~~~~~~~~~

Базовые классы и миксины для HTML тегов.

.. automodule:: html_codegen.tags.base_
   :members:
   :undoc-members:
   :show-inheritance:

Структурные теги документа
~~~~~~~~~~~~~~~~~~~~~~~~~~

Теги для создания структуры HTML документа.

.. automodule:: html_codegen.tags.document_
   :members:
   :undoc-members:
   :show-inheritance:

Семантические теги
~~~~~~~~~~~~~~~~~~

HTML5 семантические теги для улучшения структуры и доступности.

.. automodule:: html_codegen.tags.semantic_
   :members:
   :undoc-members:
   :show-inheritance:

Текстовые теги
~~~~~~~~~~~~~~

Теги для форматирования и структурирования текста.

.. automodule:: html_codegen.tags.text_
   :members:
   :undoc-members:
   :show-inheritance:

Теги списков
~~~~~~~~~~~~

Теги для создания различных типов списков.

.. automodule:: html_codegen.tags.lists_
   :members:
   :undoc-members:
   :show-inheritance:

Теги таблиц
~~~~~~~~~~~

Теги для создания HTML таблиц.

.. automodule:: html_codegen.tags.tables_
   :members:
   :undoc-members:
   :show-inheritance:

Теги форм
~~~~~~~~~

Теги для создания HTML форм и элементов ввода.

.. automodule:: html_codegen.tags.forms_
   :members:
   :undoc-members:
   :show-inheritance:

Медиа теги
~~~~~~~~~~

Теги для встраивания медиа контента.

.. automodule:: html_codegen.tags.media_
   :members:
   :undoc-members:
   :show-inheritance:

Метаданные
~~~~~~~~~~

Теги для метаданных документа.

.. automodule:: html_codegen.tags.metadata_
   :members:
   :undoc-members:
   :show-inheritance:

Интерактивные элементы
~~~~~~~~~~~~~~~~~~~~~~

Теги для создания интерактивных элементов.

.. automodule:: html_codegen.tags.interactive_
   :members:
   :undoc-members:
   :show-inheritance:

Примеры использования
----------------------

Базовое использование
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from html_codegen.tags import html, head, body, title, div, p
   
   # Создание простого документа
   with html() as doc:
       with head():
           title("Мой документ")
       with body():
           div().p().text("Привет, мир!")

Работа с атрибутами
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from html_codegen.tags import div, p
   
   # Добавление атрибутов
   with div(attrs={"class": "container", "id": "main"}):
       p(attrs={"class": "highlight"}).text("Текст")

Семантические элементы
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from html_codegen.tags import html, body, header, main, article, footer, h1, p
   
   with html() as doc:
       with body():
           with header():
               h1("Заголовок")
           with main():
               with article():
                   p("Содержание статьи")
           with footer():
               p("Подвал")

Формы
~~~~~

.. code-block:: python

   from html_codegen.tags import form, input_, label, button
   
   with form(attrs={"method": "POST"}):
       label(attrs={"for": "name"}).text("Имя:")
       input_(attrs={"type": "text", "id": "name"})
       button(attrs={"type": "submit"}).text("Отправить")

Списки
~~~~~~

.. code-block:: python

   from html_codegen.tags import ul, ol, li
   
   # Маркированный список
   with ul():
       li("Элемент 1")
       li("Элемент 2")
   
   # Нумерованный список
   with ol():
       li("Первый")
       li("Второй")

Таблицы
~~~~~~~

.. code-block:: python

   from html_codegen.tags import table, thead, tbody, tr, th, td
   
   with table():
       with thead():
           with tr():
               th("Колонка 1")
               th("Колонка 2")
       with tbody():
           with tr():
               td("Данные 1")
               td("Данные 2")
