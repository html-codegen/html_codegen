from typing import Optional

from .core import HTML


class Renderer:
    
    def __init__(self, tag: HTML, html_indent: int = 2) -> None:
        self.tag: HTML = tag
        self.html_indent = html_indent
        self._is_root: bool = tag == tag.root

    def render(self) -> str:
        if self.tag.is_text:
            return self.get_inner_text(self.tag)

        open_tag = self.get_open_tag(self.tag)
        close_tag = self.get_close_tag(self.tag)
        html = open_tag + self.get_inner_html(self.tag) + close_tag

        if self._is_root:
            html = f'<!DOCTYPE html>\n{html}'

        return html

    def get_inner_text(self, tag: HTML) -> str:
        inner_texts = []

        for string in tag._attrs.get('text', '').split('\n'):
            layer_space = self._indent_str + self._layer_space(tag.parent)
            inner_texts.append(layer_space + string)

        return '\n'.join(inner_texts)

    def get_inner_html(self, tag: HTML) -> str:
        return ''.join(self._layer_space(node) + Renderer(node).render() for node in tag.children)

    def get_close_tag(self, tag: HTML) -> str:
        if tag.is_single:
            return ''

        layer_space = self._layer_space(tag)
        if tag.children:
            layer_space = '\n' + layer_space

        return layer_space + f'</{tag.tag_name}>\n'

    def get_open_tag(self, tag: HTML) -> str:
        attrs = ''.join([
            f' {name}="{value}"'
            for name, value in tag._attrs.items()
        ])
        return f'<{tag.tag_name}{attrs}>\n'

    @property
    def _indent_str(self) -> str:
        return ' ' * self.html_indent

    def _layer_space(self, tag: Optional[HTML]) -> str:
        return self._indent_str * tag.layer if tag and not tag.is_text else ''
