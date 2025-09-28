"""
Example usage of the HTML Code Generator library.

This module demonstrates how to use the html_codegen library to create
HTML documents with various features including Brython integration.
"""

from html_codegen.tags import head, html, link, meta, style, title


def example() -> html:
    """
    Create an example HTML document demonstrating various features.

    This function shows how to use the html_codegen library to create
    a complete HTML document with head section, body content, and Brython integration.

    Returns:
        html: Complete HTML document object
    """
    html_document = html(use_brython=True)

    # First usage method (using context manager)
    with html_document:
        with head():
            meta(attrs={"charset": "UTF-8"})
            title("Aboba")
            link("https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css", rel="stylesheet")

            style("./web/styles/main.css")
            # Alternative way to include styles with less code in the resulting HTML
            # link('./web/styles/main.css', rel='stylesheet')

    # Second usage method
    body = html_document.body()
    body.div(attrs={"id": "red"})
    body.div(attrs={"id": "green"}).button().text("button")
    body.div(attrs={"id": "blue"})
    body.pyscript("web.scripts.py.hello")  # Code from ./web/scripts/py/hello.py will be executed on the page

    return html_document


if __name__ == "__main__":
    """Main entry point that creates an example document and opens it in a browser."""
    html_document = example()
    html_path = html_document.save("index.html")

    import webbrowser

    # webbrowser.open_new(f"file://{html_path}")
