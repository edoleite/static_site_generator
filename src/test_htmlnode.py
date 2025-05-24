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
    


if __name__ == "__main__":
    unittest.main(verbosity=2)