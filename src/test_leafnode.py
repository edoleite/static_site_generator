
import unittest
from htmlnode import *

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

if __name__ == "__main__":
    unittest.main(verbosity=2)