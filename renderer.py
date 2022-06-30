from typing import TYPE_CHECKING

from bs4 import BeautifulSoup as bs
import bs4.formatter

if TYPE_CHECKING:
    from core import HTML


class Renderer:
    def __init__(self, tag: 'HTML') -> None:
        self.tag = tag
        self.is_root: bool = tag == tag.root

    def render(self) -> str:
        if self.tag.is_text:
            return self.tag._attrs['text']

        doctype = '<!DOCTYPE html>' if self.is_root else ''
        inner_html = self.get_inner_html(self.tag)
        open_tag = self.get_open_tag(self.tag)
        close_tag = self.get_close_tag(self.tag)
        return bs(
            doctype + open_tag + inner_html + close_tag, features='html.parser'
        ).prettify(
            formatter=bs4.formatter.HTMLFormatter(indent=2),  # type: ignore
        )

    @staticmethod
    def get_inner_html(tag: 'HTML') -> str:
        return ''.join([
            Renderer(node).render()
            for node in tag._nodes
        ])

    @staticmethod
    def get_close_tag(tag: 'HTML') -> str:
        if tag.is_single:
            return ''
        return f'</{tag.tag_name}>'

    @staticmethod
    def get_open_tag(tag: 'HTML') -> str:
        attrs = ''.join([
            f' {name}="{value}"'
            for name, value in tag._attrs.items()
        ])
        return f'<{tag.tag_name}{attrs}>'
