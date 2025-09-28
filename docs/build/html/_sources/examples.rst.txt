Примеры использования
=====================

В этом разделе представлены различные примеры использования HTML Codegen для решения реальных задач.

Базовые примеры
---------------

Простая HTML страница
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from html_codegen.tags import html, head, body, title, div, p, h1
   
   with html() as doc:
       with head():
           title("Простая страница")
       with body():
           h1().text("Добро пожаловать!")
           div().p().text("Это пример простой HTML страницы.")
   
   from html_codegen.renderer import Renderer
   print(Renderer(doc).render())

Страница с CSS стилями
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from html_codegen.tags import html, head, body, title, link, div, p, h1
   
   with html() as doc:
       with head():
           title("Страница со стилями")
           link("styles.css", rel="stylesheet")
       with body():
           with div(attrs={"class": "container"}):
               h1().text("Стилизованная страница")
               with div(attrs={"class": "highlight"}):
                   p().text("Этот текст выделен стилем.")
   
   from html_codegen.renderer import Renderer
   print(Renderer(doc).render())

Продвинутые примеры
-------------------

Блог с несколькими статьями
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from html_codegen.tags import (
       html, head, body, title, meta, link, 
       header, nav, main, article, aside, footer,
       h1, h2, p, ul, li, a, time
   )
   
   with html() as blog:
       with head():
           title("Мой блог")
           meta(attrs={"charset": "UTF-8"})
           meta(attrs={"name": "viewport", "content": "width=device-width, initial-scale=1.0"})
           link("styles.css", rel="stylesheet")
       
       with body():
           with header():
               h1().text("Мой блог")
               with nav():
                       with ul():
                           with li():
                               a(attrs={"href": "/"}).text("Главная")
                           with li():
                               a(attrs={"href": "/about"}).text("О нас")
                           with li():
                               a(attrs={"href": "/contact"}).text("Контакты")
           
           with main():
               with article():
                   h2().text("Первая статья")
                   p().text("Содержание первой статьи...")
                   time(attrs={"datetime": "2024-01-15"}).text("2024-01-15")
               
               with article():
                   h2().text("Вторая статья")
                   p().text("Содержание второй статьи...")
                   time(attrs={"datetime": "2024-01-20"}).text("2024-01-20")
           
           with aside():
               h2().text("Боковая панель")
               p().text("Дополнительная информация...")
           
           with footer():
               p().text("© 2024 Мой блог. Все права защищены.")
   
   from html_codegen.renderer import Renderer
   print(Renderer(blog).render())

Форма регистрации
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from html_codegen.tags import (
       html, head, body, title, form, fieldset, legend,
       label, input_, select, option, textarea, button, div, h1
   )
   
   with html() as registration_form:
       with head():
           title("Регистрация")
       
       with body():
           h1().text("Регистрация нового пользователя")
           
           with form(attrs={"method": "POST", "action": "/register"}):
               with fieldset():
                   legend().text("Личная информация")
                   
                   with div():
                       label(attrs={"for": "first_name"}).text("Имя:")
                       input_(attrs={"type": "text", "id": "first_name", "name": "first_name", "required": ""})
                   
                   with div():
                       label(attrs={"for": "last_name"}).text("Фамилия:")
                       input_(attrs={"type": "text", "id": "last_name", "name": "last_name", "required": ""})
                   
                   with div():
                       label(attrs={"for": "email"}).text("Email:")
                       input_(attrs={"type": "email", "id": "email", "name": "email", "required": ""})
                   
                   with div():
                       label(attrs={"for": "password"}).text("Пароль:")
                       input_(attrs={"type": "password", "id": "password", "name": "password", "required": ""})
                   
                   with div():
                       label(attrs={"for": "confirm_password"}).text("Подтверждение пароля:")
                       input_(attrs={"type": "password", "id": "confirm_password", "name": "confirm_password", "required": ""})
               
               with fieldset():
                   legend().text("Дополнительная информация")
                   
                   with div():
                       label(attrs={"for": "country"}).text("Страна:")
                       with select(attrs={"id": "country", "name": "country"}):
                           option(attrs={"value": ""}).text("Выберите страну")
                           option(attrs={"value": "ru"}).text("Россия")
                           option(attrs={"value": "us"}).text("США")
                           option(attrs={"value": "de"}).text("Германия")
                   
                   with div():
                       label(attrs={"for": "bio"}).text("О себе:")
                       textarea(attrs={"id": "bio", "name": "bio", "rows": "4", "cols": "50"})
               
               button(attrs={"type": "submit"}).text("Зарегистрироваться")
   
   from html_codegen.renderer import Renderer
   print(Renderer(registration_form).render())

Таблица данных
~~~~~~~~~~~~~~

.. code-block:: python

   from html_codegen.tags import (
       html, head, body, title, table, thead, tbody, tfoot,
       tr, th, td, caption, h1, div
   )
   
   with html() as data_table:
       with head():
           title("Таблица данных")
       
       with body():
           h1().text("Отчет по продажам")
           
           with div(attrs={"class": "table-container"}):
               with table(attrs={"border": "1", "cellpadding": "8", "cellspacing": "0"}):
                   caption().text("Продажи по месяцам")
                   
                   with thead():
                       with tr():
                           th().text("Месяц")
                           th().text("Продажи")
                           th().text("Прибыль")
                           th().text("Рост")
                   
                   with tbody():
                       with tr():
                           td().text("Январь")
                           td().text("100,000")
                           td().text("20,000")
                           td().text("+5%")
                       
                       with tr():
                           td().text("Февраль")
                           td().text("120,000")
                           td().text("25,000")
                           td().text("+8%")
                       
                       with tr():
                           td().text("Март")
                           td().text("110,000")
                           td().text("22,000")
                           td().text("+3%")
                   
                   with tfoot():
                       with tr():
                           th().text("Итого")
                           th().text("330,000")
                           th().text("67,000")
                           th().text("+5.3%")
   
   from html_codegen.renderer import Renderer
   print(Renderer(data_table).render())

Интерактивные примеры
---------------------

Простая галерея изображений
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from html_codegen.tags import (
       html, head, body, title, div, img, h1, p, 
       script, link
   )
   
   with html() as gallery:
       with head():
           title("Галерея изображений")
           link("gallery.css", rel="stylesheet")
       
       with body():
           h1().text("Моя галерея")
           
           with div(attrs={"class": "gallery"}):
               img(attrs={"src": "image1.jpg", "alt": "Изображение 1", "onclick": "openModal(this)"})
               img(attrs={"src": "image2.jpg", "alt": "Изображение 2", "onclick": "openModal(this)"})
               img(attrs={"src": "image3.jpg", "alt": "Изображение 3", "onclick": "openModal(this)"})
           
           script(src="gallery.js")
   
   from html_codegen.renderer import Renderer
   print(Renderer(gallery).render())

Интеграция с Brython
--------------------

Пример для выполнения в браузере
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from html_codegen.tags import html, head, body, title, pyscript, div, button, p, h1

   
   with html(use_brython=True) as brython_app:
       with head() as head_tag:
           title("Brython приложение")
       
       with body() as body_tag:
           h1().text("Интерактивное приложение")
           
           with div(attrs={"id": "app"}):
               p().text("Нажмите кнопку для взаимодействия")
               button(attrs={"id": "btn"}).text("Кликни меня")
               p(attrs={"id": "result"})
           
           pyscript("brython_app")
   
   from html_codegen.renderer import Renderer
   print(Renderer(brython_app).render())

Полезные паттерны
-----------------

Создание компонентов
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def create_card(title, content, image_url=None):
       """Создает карточку с заголовком и содержимым."""
       from html_codegen.tags import div, h3, p, img
       
       with div(attrs={"class": "card"}):
           if image_url:
               img(attrs={"src": image_url, "alt": title, "class": "card-image"})
           h3(attrs={"class": "card-title"}).text(title)
           p(attrs={"class": "card-content"}).text(content)
   
   # Использование компонента
   from html_codegen.tags import html, head, body, title, h1
   
   with html() as cards_page:
       with head():
           title("Карточки")
       
       with body():
           h1().text("Наши услуги")
           
           create_card("Веб-разработка", "Создание современных веб-сайтов", "web.jpg")
           create_card("Мобильные приложения", "Разработка iOS и Android приложений", "mobile.jpg")
           create_card("Консультации", "Технические консультации и аудит", "consulting.jpg")
   
   from html_codegen.renderer import Renderer
   print(Renderer(cards_page).render())

Динамическое создание контента
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def create_navigation_menu(items):
       """Создает навигационное меню из списка элементов."""
       from html_codegen.tags import nav, ul, li, a
       
       with nav(attrs={"class": "main-nav"}):
           with ul():
               for item in items:
                   with li():
                       a(attrs={"href": item["url"]}).text(item["text"])
   
   # Использование
   menu_items = [
       {"text": "Главная", "url": "/"},
       {"text": "О нас", "url": "/about"},
       {"text": "Услуги", "url": "/services"},
       {"text": "Контакты", "url": "/contact"}
   ]
   
   from html_codegen.tags import html, head, body, title, h1, p
   
   with html() as nav_page:
       with head():
           title("Страница с навигацией")
       
       with body():
           create_navigation_menu(menu_items)
           h1().text("Контент страницы")
           p().text("Основное содержимое...")
   
   from html_codegen.renderer import Renderer
   print(Renderer(nav_page).render())
