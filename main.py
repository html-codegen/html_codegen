from core import HTML
from renderer import Renderer
from pathlib import Path


def example():
    html_path = Path(__name__).parent.resolve() / 'index.html'
    bootstrap_href = 'https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css'

    html = HTML()
    head = html.head()
    body = html.body(**{'class': 'container'})

    head.meta(charset='UTF-8')
    head.link(
        href=bootstrap_href,
        rel='stylesheet',
    )
    head.title().text(text='Aboba')

    form = body.div(**{'class': 'row justify-content-center'}).form(**{'class': 'col-4'})
    with form:
        username = HTML('div', **{'class': 'form-group'})
        username.label(**{'name': 'username'}).text(text='Username')
        username.input(**{'id': 'username', 'name': 'username', 'class': 'form-control'})

        password = HTML('div', **{'class': 'form-group'})
        password.label(**{'name': 'password'}).text(text='Password')
        password.input(**{'name': 'password', 'type': 'password', 'class': 'form-control'})

        HTML('button', **{'type': 'submit', 'class': 'btn btn-primary'}).text(text='Login')

    with open(html_path, 'w') as file_:
        renderer = Renderer(html)
        file_.write(renderer.render())

    return html_path


if __name__ == "__main__":
    html_path = example()

    import webbrowser
    webbrowser.open_new_tab(f'file://{html_path}')
