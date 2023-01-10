from html_codegen.tags import head, html, link, meta, style, title


def example() -> html:
    html_document = html(use_brython=True)

    # Первый вариант использования(через контекстный менеджер)
    with html_document:
        with head():
            meta(attrs={'charset': 'UTF-8'})
            title('Aboba')
            link('https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css', rel='stylesheet')

            style('./web/styles/main.css')
            # А можно так подключить стили, и кода в исходном html будет меньше
            # link('./web/styles/main.css', rel='stylesheet')

    # Второй вариант использования
    body = html_document.body()
    body.div(attrs={'id': 'red'})
    body.div(attrs={'id': 'green'}).button().text('button')
    body.div(attrs={'id': 'blue'})
    body.pyscript('web.scripts.py.hello') # на странице исполнится код из ./web/scripts/py/hello.py

    return html_document


if __name__ == '__main__':
    html_document = example()
    html_path = html_document.save('index.html')

    import webbrowser
    webbrowser.open_new(f'file://{html_path}')
