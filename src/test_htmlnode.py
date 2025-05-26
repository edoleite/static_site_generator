import unittest
from htmlnode import *

class TestHtmlNode(unittest.TestCase):
    def test_properties_assignment(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://example.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click me")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"href": "https://example.com"})

    def test_default_empty_children_and_props(self):
        node = HTMLNode("p", "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_nested_children_structure(self):
        child1 = HTMLNode("b", "bold")
        child2 = HTMLNode("i", "italic")
        parent = HTMLNode("div", None, [child1, child2], {"class": "richtext"})
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0].tag, "b")
        self.assertEqual(parent.children[1].value, "italic")
        self.assertEqual(parent.props.get("class"), "richtext")

    def test_repr(self):
        child = HTMLNode("span", "child")
        node = HTMLNode("div", "parent", [child], {"class": "box"})
        expected = (
            "HTMLNode(tag='div', value='parent', "
            "children=[HTMLNode(tag='span', value='child', children=[], props={})], "
            "props={'class': 'box'})"
        )
        self.assertEqual(repr(node), expected)

class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
            node = LeafNode("p", "Hello, world!")
            self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_anchor_tag(self):
        node = LeafNode(tag="a", value="Google", props={"href": "https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">Google</a>')

    def test_no_tag_returns_value(self):
        node = LeafNode(value="Sadece metin")
        self.assertEqual(node.to_html(), "Sadece metin")
        
    def test_missing_value_raises_error(self):
        node = LeafNode(tag="p")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_anchor_missing_href_raises_error(self):
        node = LeafNode(tag="a", value="Link yok", props={})
        with self.assertRaises(ValueError):
            node.to_html()

class DummyChild:
    # Simulate an object that has to_html method
    def to_html(self):
        return "<dummy>ok</dummy>"

class TestParentNodeExtended(unittest.TestCase):
    def test_props_are_stored_correctly(self):
        props = {"class": "test-div"}
        parent = ParentNode(tag="div", children=[LeafNode("span", "hello")], props=props)
        self.assertEqual(parent.props, props)

    def test_props_are_ignored_in_output(self):
        # Props exist but not rendered
        parent = ParentNode(tag="div", children=[LeafNode("i", "italic")], props={"id": "test"})
        self.assertEqual(parent.to_html(), "<div><i>italic</i></div>")

    def test_child_without_to_html_raises(self):
        class BadChild:
            pass  # Missing to_html()

        parent = ParentNode(tag="div", children=[BadChild()])
        with self.assertRaises(AttributeError):
            parent.to_html()

    def test_child_returns_non_string_raises(self):
        class BadChild:
            def to_html(self):
                return None  # should raise TypeError in ParentNode

        parent = ParentNode(tag="div", children=[BadChild()])

        with self.assertRaises(TypeError):  # Bu satırdan itibaren hata bekleniyor
            parent.to_html()

    def test_none_in_children_raises(self):
        parent = ParentNode(tag="div", children=[None])
        with self.assertRaises(AttributeError):
            parent.to_html()

    def test_children_with_mixed_valid_and_dummy(self):
        child1 = LeafNode(tag="b", value="bold")
        child2 = DummyChild()
        parent = ParentNode(tag="div", children=[child1, child2])
        self.assertEqual(parent.to_html(), "<div><b>bold</b><dummy>ok</dummy></div>")

    def test_empty_string_tag_raises(self):
        child = LeafNode(tag="b", value="bold")
        with self.assertRaises(ValueError):
            ParentNode(tag="", children=[child]).to_html()

    def test_none_tag_raises(self):
        child = LeafNode(tag="b", value="bold")
        with self.assertRaises(ValueError):
            ParentNode(tag=None, children=[child]).to_html()

    def test_children_list_contains_non_node(self):
        child = LeafNode(tag="i", value="italic")
        parent = ParentNode(tag="div", children=[child, 123])  # 123 is invalid
        with self.assertRaises(AttributeError):
            parent.to_html()

if __name__ == "__main__":
    unittest.main(verbosity=2)