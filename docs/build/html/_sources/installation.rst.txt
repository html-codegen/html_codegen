Установка
=========

HTML Codegen можно установить несколькими способами в зависимости от ваших потребностей.

Требования
----------

* Python 3.12 или выше
* uv (рекомендуется) или pip для управления зависимостями

Установка через uv (рекомендуется)
-----------------------------------

1. Клонируйте репозиторий:

.. code-block:: bash

   git clone https://gitlab.com/html_codegen/html_codegen.git
   cd html_codegen

2. Создайте виртуальное окружение и установите зависимости:

.. code-block:: bash

   python3 -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   uv sync

Установка через pip
-------------------

1. Клонируйте репозиторий:

.. code-block:: bash

   git clone https://gitlab.com/html_codegen/html_codegen.git
   cd html_codegen

2. Создайте виртуальное окружение:

.. code-block:: bash

   python3 -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate

3. Установите зависимости:

.. code-block:: bash

   pip install -e .

Установка для разработки
-------------------------

Для разработки и тестирования установите дополнительные зависимости:

.. code-block:: bash

   uv sync --group dev

Или с pip:

.. code-block:: bash

   pip install -e ".[dev]"

Зависимости для разработки включают:
* Sphinx - для генерации документации
* pytest - для тестирования
* black - для форматирования кода
* ruff - для линтинга
* pyright - для проверки типов

Проверка установки
------------------

После установки проверьте, что библиотека работает корректно:

.. code-block:: python

   from html_codegen import html, head, body, title, div, p
   
   # Простой тест
   with html() as doc:
       with head():
           title("Тест")
       with body():
           div().p().text("Установка прошла успешно!")
   
   print(doc.render())

Если код выполняется без ошибок, установка прошла успешно.

Устранение проблем
------------------

**Ошибка импорта модуля**
   Убедитесь, что вы находитесь в корневой директории проекта и активировали виртуальное окружение.

**Ошибки зависимостей**
   Убедитесь, что все зависимости установлены корректно. Попробуйте переустановить зависимости:

   .. code-block:: bash

      uv sync --reinstall

**Проблемы с Brython**
   Brython не является обязательной зависимостью для базовой функциональности. 
   Интеграция с Brython требуется только для клиентского выполнения Python кода в браузере.
