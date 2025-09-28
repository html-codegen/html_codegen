"""
HTML rendering engine for converting HTML node trees to formatted HTML strings.

This module provides the Renderer class which handles the conversion of HTML node
structures into properly formatted HTML markup with indentation and structure.
"""
from typing import Optional

from .core import HTML


class Renderer:
    """
    HTML renderer for converting HTML node trees to formatted HTML strings.
    
    This class handles the conversion of HTML node structures into properly
    formatted HTML markup with customizable indentation.
    
    Attributes:
        tag (HTML): The HTML node to render
        html_indent (int): Number of spaces for indentation (default: 2)
        _is_root (bool): Whether this tag is the root of the document
    """
    
    def __init__(self, tag: HTML, html_indent: int = 2) -> None:
        """
        Initialize the renderer with an HTML tag and indentation settings.
        
        Args:
            tag (HTML): The HTML node to render
            html_indent (int): Number of spaces for indentation (default: 2)
        """
        self.tag: HTML = tag
        self.html_indent = html_indent
        self._is_root: bool = tag == tag.root

    def render(self) -> str:
        """
        Render the HTML tag and its children to a formatted HTML string.
        
        Returns:
            str: Formatted HTML string
        """
        if self.tag.is_text:
            return self.get_inner_text(self.tag)

        open_tag = self.get_open_tag(self.tag)
        close_tag = self.get_close_tag(self.tag)
        html = open_tag + self.get_inner_html(self.tag) + close_tag

        if self._is_root:
            html = f'<!DOCTYPE html>\n{html}'

        return html

    def get_inner_text(self, tag: HTML) -> str:
        """
        Get the inner text content of a tag with proper indentation.
        
        Args:
            tag (HTML): The HTML tag to get text from
            
        Returns:
            str: Formatted inner text
        """
        inner_texts = []

        for string in tag._attrs.get('text', '').split('\n'):
            layer_space = self._indent_str + self._layer_space(tag.parent)
            inner_texts.append(layer_space + string)

        return '\n'.join(inner_texts)

    def get_inner_html(self, tag: HTML) -> str:
        """
        Get the inner HTML content of a tag with proper indentation.
        
        Args:
            tag (HTML): The HTML tag to get inner HTML from
            
        Returns:
            str: Formatted inner HTML
        """
        return ''.join(self._layer_space(node) + Renderer(node).render() for node in tag.children)

    def get_close_tag(self, tag: HTML) -> str:
        """
        Get the closing tag for an HTML element.
        
        Args:
            tag (HTML): The HTML tag to get closing tag for
            
        Returns:
            str: Formatted closing tag
        """
        if tag.is_single:
            return ''

        layer_space = self._layer_space(tag)
        if tag.children:
            layer_space = '\n' + layer_space

        return layer_space + f'</{tag.tag_name}>\n'

    def get_open_tag(self, tag: HTML) -> str:
        """
        Get the opening tag for an HTML element with attributes.
        
        Args:
            tag (HTML): The HTML tag to get opening tag for
            
        Returns:
            str: Formatted opening tag
        """
        attrs = ''.join([
            f' {name}="{value}"'
            for name, value in tag._attrs.items()
        ])
        return f'<{tag.tag_name}{attrs}>\n'

    @property
    def _indent_str(self):
        """Get the indentation string based on html_indent setting."""
        return ' ' * self.html_indent

    def _layer_space(self, tag: Optional[HTML]) -> str:
        """
        Calculate the appropriate spacing for a tag based on its layer.
        
        Args:
            tag (Optional[HTML]): The HTML tag to calculate spacing for
            
        Returns:
            str: Appropriate spacing string
        """
        return self._indent_str * tag.layer if tag and not tag.is_text else ''
