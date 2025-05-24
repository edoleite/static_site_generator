import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is another text node", TextType.LINK, "www.test.com" )
        node2 = TextNode("This is another text node", TextType.LINK, "www.test.com")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("what the fuck dude", TextType.CODE )
        node2 = TextNode("hello", TextType.CODE)
        self.assertNotEqual(node, node2)   


if __name__ == "__main__":
    unittest.main(verbosity=2)