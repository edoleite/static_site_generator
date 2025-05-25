import unittest
from htmlnode import *
from textnode import *
from main import *

class TestTextnodetoHtmlnode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("", TextType.LINK, "www.noktanokta.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "www.noktanokta.com"})

    def test_image(self):
        node = TextNode("A beautiful image", TextType.IMAGE, "www.thisisanimage.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "www.thisisanimage.com", "alt": "A beautiful image"})
        self.assertEqual(html_node.value, "")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")

    def test_invalid_type_raises(self):
        class FakeType:
            pass
        node = TextNode("Some text", FakeType())
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertIn("invalid text type", str(context.exception))




if __name__ == "__main__":
    unittest.main(verbosity=2)