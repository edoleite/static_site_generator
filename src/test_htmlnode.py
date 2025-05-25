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

if __name__ == "__main__":
    unittest.main(verbosity=2)