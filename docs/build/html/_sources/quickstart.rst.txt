Быстрый старт
=============

Это руководство поможет вам быстро начать работу с HTML Codegen.

Основные концепции
------------------

HTML Codegen использует несколько ключевых концепций:

1. **Контекстные менеджеры** - для создания иерархических структур
2. **Динамические теги** - создание HTML элементов через вызовы методов
3. **Древовидная структура** - HTML узлы организованы как дерево

Первый пример
-------------

Создадим простую HTML страницу:

.. code-block:: python

   from html_codegen.tags import html, head, body, title, div, p, h1
    
   with html() as doc:
       with head():
           title("Моя первая страница")
       with body():
           h1().text("Добро пожаловать!")
           div().p().text("Это мой первый пример с HTML Codegen.")
   
   from html_codegen.renderer import Renderer
   print(Renderer(doc).render())

Результат:

.. code-block:: html

   <html>
   <head>
   <title>Моя первая страница</title>
   </head>
   <body>
   <h1>Добро пожаловать!</h1>
   <div>
   <p>Это мой первый пример с HTML Codegen.</p>
   </div>
   </body>
   </html>

Работа с атрибутами
-------------------

Добавляйте атрибуты к HTML элементам:

.. code-block:: python

   from html_codegen.tags import html, body, div, p
   
   with html() as doc:
       with body():
           with div(attrs={"class": "container", "id": "main"}):
               p(attrs={"class": "highlight"}).text("Текст с атрибутами")
   
   from html_codegen.renderer import Renderer
   print(Renderer(doc).render())

Результат:

.. code-block:: html

   <html>
   <body>
   <div class="container" id="main">
   <p class="highlight">Текст с атрибутами</p>
   </div>
   </body>
   </html>

Семантические элементы
----------------------

Используйте семантические HTML5 элементы:

.. code-block:: python

   from html_codegen.tags import html, head, body, title, header, main, article, section, footer, h1, h2, p
   
   with html() as doc:
       with head():
           title("Семантическая страница")
       with body():
           with header():
               h1().text("Заголовок сайта")
           with main():
               with article():
                   h2().text("Статья")
                   section().text("Содержание статьи")
           with footer():
               p().text("Подвал сайта")
   
   from html_codegen.renderer import Renderer
   print(Renderer(doc).render())

Формы
-----

Создавайте HTML формы:

.. code-block:: python

   from html_codegen.tags import html, body, form, input_, label, button
   
   with html() as doc:
       with body():
           with form(attrs={"method": "POST", "action": "/submit"}):
               label(attrs={"for": "name"}).text("Имя:")
               input_(attrs={"type": "text", "id": "name", "name": "name"})
               button(attrs={"type": "submit"}).text("Отправить")
   
   from html_codegen.renderer import Renderer
   print(Renderer(doc).render())

Списки
------

Создавайте различные типы списков:

.. code-block:: python

   from html_codegen.tags import html, body, ul, ol, li, h2
   
   with html() as doc:
       with body():
           h2().text("Нумерованный список:")
           with ol():
               li().text("Первый элемент")
               li().text("Второй элемент")
               li().text("Третий элемент")
           
           h2().text("Маркированный список:")
           with ul():
               li().text("Элемент 1")
               li().text("Элемент 2")
               li().text("Элемент 3")
   
   from html_codegen.renderer import Renderer
   print(Renderer(doc).render())

Таблицы
-------

Создавайте HTML таблицы:

.. code-block:: python

   from html_codegen.tags import html, body, table, thead, tbody, tr, th, td
   
   with html() as doc:
       with body():
           with table(attrs={"border": "1"}):
               with thead():
                   with tr():
                       th().text("Имя")
                       th().text("Возраст")
                       th().text("Город")
               with tbody():
                   with tr():
                       td().text("Иван")
                       td().text("25")
                       td().text("Москва")
                   with tr():
                       td().text("Мария")
                       td().text("30")
                       td().text("Санкт-Петербург")
   
   from html_codegen.renderer import Renderer
   print(Renderer(doc).render())

Следующие шаги
--------------

Теперь, когда вы изучили основы, вы можете:

* Изучить :doc:`api` для полного списка доступных тегов
* Посмотреть :doc:`examples` для более сложных примеров
* Изучить интеграцию с Brython для клиентского выполнения

Полезные советы
---------------

1. **Используйте контекстные менеджеры** - они обеспечивают правильную структуру HTML
2. **Проверяйте результат** - используйте ``print(doc.render())`` для просмотра сгенерированного HTML
3. **Изучайте атрибуты** - многие HTML элементы поддерживают стандартные атрибуты
4. **Используйте семантические теги** - они делают HTML более понятным и доступным
