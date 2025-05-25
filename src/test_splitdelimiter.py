import unittest
from textnode import TextNode, TextType
from functions import split_nodes_delimiter  # Adjust import path if needed

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_split(self):
        nodes = [TextNode("This is a =test= sentence", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "=", TextType.BOLD)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        self.assertEqual(result[1].text, "test")
        self.assertEqual(result[1].text_type, TextType.BOLD)

        self.assertEqual(result[2].text, " sentence")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_multiple_delimiters(self):
        nodes = [TextNode("A =bold= and =strong= test", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "=", TextType.BOLD)

        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "A ")
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[3].text, "strong")
        self.assertEqual(result[4].text, " test")

    def test_node_with_no_delimiter_is_kept_as_is(self):
        nodes = [TextNode("This is normal text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is normal text")
        self.assertEqual(result[0].text_type, TextType.TEXT)


    def test_non_text_nodes_are_untouched(self):
        node1 = TextNode("bold", TextType.BOLD)
        node2 = TextNode("italic", TextType.ITALIC)
        old_nodes = [node1, node2]
        result = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], node1)
        self.assertEqual(result[1], node2)



if __name__ == "__main__":
    unittest.main(verbosity=2)
