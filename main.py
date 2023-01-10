from pathlib import Path

from src.core import HTML
from src.renderer import Renderer
from src.tags import head, meta, script, title


def example() -> Renderer:
    brython_paths = [
        "brython_source/brython.js",
        "brython_source/brython_stdlib.js",
    ]

    html = HTML()

    # Первый вариант использования(через контекстный менеджер)
    with html:
        with head():
            meta(attrs={'charset': 'UTF-8'})
            title().text(attrs={'text': 'Aboba'})
            for brython_path in brython_paths:
                script(attrs={'type': 'text/javascript', 'src': brython_path})

    # Второй вариант использования
    body = html.body(attrs={'class': 'container', 'onload': 'brython()', 'style': 'height: 100vh;'})
    body.div(attrs={'style': 'background-color: red; height: 30%;'})
    body.div(attrs={'style': 'background-color: green; height: 30%;'})
    body.div(attrs={'style': 'background-color: blue; height: 30%;'})
    body.pyscript('brython_scripts.hello') # на странице исполнится код из ./brython_scripts/hello.py

    return Renderer(html)


if __name__ == "__main__":
    renderer = example()
    html_path = Path(__name__).parent.resolve() / 'index.html'
    html_text = renderer.render()

    with open(html_path, 'w') as f:
        f.write(html_text)

    import webbrowser
    webbrowser.open_new(f'file://{html_path}')
