import unittest
from htmlnode import *




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
    unittest.main()



