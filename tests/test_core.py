import pytest

from html_codegen import HTML, HTMLNode, html, head, body, div, p, text
from html_codegen.exceptions import (
    NodeAlreadyHasParentError,
    TextNodeNestingError,
    SingleTagNestingError,
    TagOutsideHtmlError,
    DuplicateTagError,
    BrythonNotEnabledError,
)


class TestHTMLNode:
    def test_node_has_no_parent_initially(self):
        node = HTMLNode()
        assert node.parent is None

    def test_node_can_add_child(self):
        parent = HTMLNode()
        child = HTMLNode()
        parent.add_node(child)
        assert child.parent == parent
        assert child in parent._nodes

    def test_node_cannot_be_added_twice(self):
        parent1 = HTMLNode()
        parent2 = HTMLNode()
        child = HTMLNode()
        parent1.add_node(child)
        with pytest.raises(NodeAlreadyHasParentError):
            parent2.add_node(child)


class TestHTML:
    def test_html_tag_name(self):
        doc = html()
        assert doc.tag_name == "html"

    def test_html_with_brython(self):
        doc = html(use_brython=True)
        assert doc.use_brython is True

    def test_html_without_brython(self):
        doc = html()
        assert doc.use_brython is False


class TestText:
    def test_text_content(self):
        t = text("Hello World")
        assert t._attrs.get("text") == "Hello World"

    def test_text_is_text(self):
        t = text("Hello")
        assert t.is_text is True

    def test_text_cannot_have_children(self):
        t = text("Hello")
        with pytest.raises(TextNodeNestingError):
            t.add_node(HTMLNode())


class TestSingleTag:
    def test_single_tag_is_single(self):
        from html_codegen.tags import img
        i = img()
        assert i.is_single is True

    def test_single_tag_cannot_have_children(self):
        from html_codegen.tags import img
        i = img()
        with pytest.raises(SingleTagNestingError):
            i.add_node(HTMLNode())


class TestContextManager:
    def test_context_manager_adds_children(self):
        with html() as doc:
            with head():
                pass
        
        assert len(doc.children) == 1
        assert doc.children[0].tag_name == "head"


class TestDynamicTagCreation:
    def test_dynamic_tag_creation(self):
        doc = html()
        doc.body()
        assert len(doc.children) == 1
        assert doc.children[0].tag_name == "body"

    def test_chained_tag_creation(self):
        doc = html()
        body = doc.body()
        body.div().p().text("Hello")
        
        assert len(body.children) == 1
        div_tag = body.children[0]
        assert div_tag.tag_name == "div"
        assert len(div_tag.children) == 1


class TestExceptions:
    def test_node_already_has_parent_message(self):
        parent1 = HTMLNode()
        parent2 = HTMLNode()
        child = HTMLNode()
        parent1.add_node(child)
        
        with pytest.raises(NodeAlreadyHasParentError) as exc_info:
            parent2.add_node(child)
        
        assert "already has parent" in str(exc_info.value)
