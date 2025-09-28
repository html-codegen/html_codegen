"""
HTML Code Generator - A Python library for generating HTML documents programmatically.

This module provides a simple and intuitive way to create HTML documents using Python classes
and context managers. It supports all standard HTML5 tags and provides a clean API for
building complex document structures.

Key Features:
- Context manager support for clean, readable code
- Dynamic tag creation through method calls
- Support for all HTML5 semantic elements
- Brython integration for client-side Python execution
- Type hints throughout the codebase

Example:
    from html_codegen import html, head, body, title, div, p
    
    with html() as doc:
        with head():
            title("My Page")
        with body():
            div().p("Hello, World!")

The library is organized into several modules:
- core: Base HTML node classes and document structure
- renderer: HTML rendering and formatting
- tags: Individual HTML tag implementations organized by category
"""
