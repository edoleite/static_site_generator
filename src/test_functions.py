import unittest
from htmlnode import *
from textnode import *
from functions import *
from blocknode import *

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

class TestTextnodetoHtmlnode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
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

class TestMarkdownExtractors(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_single_image(self):
        text = "Here is an image ![alt](image.png)"
        self.assertEqual(extract_markdown_images(text), [("alt", "image.png")])
    
    def test_multiple_images(self):
        text = "![img1](1.png) some text ![img2](2.jpg)"
        self.assertEqual(extract_markdown_images(text), [("img1", "1.png"), ("img2", "2.jpg")])

    def test_image_no_alt_text(self):
        text = "Check this ![](pic.png)"
        self.assertEqual(extract_markdown_images(text), [("", "pic.png")])

    def test_image_with_spaces(self):
        text = "![Alt Text Here](http://example.com/image.png)"
        self.assertEqual(extract_markdown_images(text), [("Alt Text Here", "http://example.com/image.png")])

    def test_single_link(self):
        text = "Click [here](https://example.com)"
        self.assertEqual(extract_markdown_links(text), [("here", "https://example.com")])

    def test_multiple_links(self):
        text = "[Google](https://google.com) and [GitHub](https://github.com)"
        self.assertEqual(extract_markdown_links(text), [
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com"),
        ])

    def test_links_and_images_mixed(self):
        text = "![img](img.png) and [link](link.com)"
        self.assertEqual(extract_markdown_images(text), [("img", "img.png")])
        self.assertEqual(extract_markdown_links(text), [("link", "link.com")])

    def test_ignores_malformed(self):
        text = "![alt(image.png) and [text](link.com"
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])

    def test_ignores_image_in_links(self):
        text = "![alt](img.png) and ![a](b.jpg) and [not image](url.com)"
        self.assertEqual(extract_markdown_links(text), [("not image", "url.com")])
        self.assertEqual(extract_markdown_images(text), [("alt", "img.png"), ("a", "b.jpg")])

class TestSplitters(unittest.TestCase):
    #test for a single node list
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    #test for a multiple node list
    def test_split_images_2(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        node2 = TextNode(
            "This is another text with an ![image2](https://i.imgur2.com/zjjcJKZ.png) and another ![second image2](https://i.imgur2.com/3elNhQu.png)",
            TextType.TEXT
        )

        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),

                TextNode("This is another text with an ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "https://i.imgur2.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image2", TextType.IMAGE, "https://i.imgur2.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    #test for a empty list
    def test_split_images_3(self):
        node = []
        new_nodes = split_nodes_image(node)
        self.assertEqual([], new_nodes)
    #test for a node list that isnt text type
    def test_split_images_4(self):
        node = TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        new_nodes = split_nodes_image([node])
        self.assertEqual([node], new_nodes)
    #test for node not including an image
    def test_split_images_5(self):
        node = TextNode("image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual([node], new_nodes)
    
    def test_split_images_6(self):
        node = TextNode("", TextType.TEXT)
        node2 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node, node2])
        self.assertEqual([TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )], new_nodes)
        
    
    def test_split_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_single_link(self):
        node = TextNode("This is a [link](http://example.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "This is a ")
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "http://example.com")

    def test_multiple_links(self):
        node = TextNode("Start [one](1.com) middle [two](2.com) end", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Start ")
        self.assertEqual(result[1].text, "one")
        self.assertEqual(result[1].url, "1.com")
        self.assertEqual(result[2].text, " middle ")
        self.assertEqual(result[3].text, "two")
        self.assertEqual(result[3].url, "2.com")
        self.assertEqual(result[4].text, " end")

    def test_link_with_empty_text(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])  # tek boş node varsa geri dönsün

    def test_mixed_nodes(self):
        nodes = [
            TextNode("Hello [world](url.com)", TextType.TEXT),
            TextNode("Just bold", TextType.BOLD),
            TextNode("", TextType.TEXT)
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Hello ")
        self.assertEqual(result[1].text, "world")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[2].text, "Just bold")
        self.assertEqual(result[2].text_type, TextType.BOLD)

    def test_no_links(self):
        node = TextNode("This is just text", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_link_at_start_and_end(self):
        node = TextNode("[start](s.com) middle [end](e.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "start")
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[1].text, " middle ")
        self.assertEqual(result[2].text, "end")
        self.assertEqual(result[2].text_type, TextType.LINK)

    def test_texttotextnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], text_nodes
        )

    def test_bold_only(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ])

    def test_italic_only(self):
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ])

    def test_code_only(self):
        text = "This is `code` block"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT)
        ])

    def test_link_only(self):
        text = "Go to [Google](https://google.com)"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("Go to ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com")
        ])

    def test_image_only(self):
        text = "Here is an image ![Alt](img.jpg)"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("Alt", TextType.IMAGE, "img.jpg")
        ])

    def test_all_formats_combined(self):
        text = "**bold**, _italic_, `code`, [link](url), ![alt](img)"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(", ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "img")
        ])

    def test_empty_string(self):
        text = ""
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode("", TextType.TEXT)])    
    
    def test_no_markdown(self):
        text = "Just plain text."
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode("Just plain text.", TextType.TEXT)])
    
    def test_unclosed_bold(self):
        text = "This is **bold"
        with self.assertRaises(Exception) as context:
            text_to_textnodes(text)
        self.assertIn("Text does not have delimiter", str(context.exception))    

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_empty_blocks(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_list_with_whitespaces(self):
        md = """
    This is **bolded** paragraph
    
    

    This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line        
    
    
    
    
    
            - This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks222(self):
        md = "  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

    def test_block_to_block_type(self):
        md = """
    This is **bolded** paragraph
    
    

    This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line        
    
    
    
    
    
            - This is a list
- with items


1. this is an ordered list
2. list item number two
3. list item number three


> this is a quote block
> quote block continues


```
here is a code block
bunch of codes here
```
    """
        blocks = markdown_to_blocks(md)
        list_of_block_types = [block_to_block_type(block) for block in blocks]
        self.assertEqual(
            list_of_block_types,
            [BlockType.PARAGRAPH, BlockType.PARAGRAPH, BlockType.ULIST, BlockType.OLIST, BlockType.QUOTE, BlockType.CODE ]
        )

class TestMarkdownConversion(unittest.TestCase):
    def test_heading_conversion(self):
        block = "# Heading"
        tag = determine_tag(block)
        self.assertEqual(tag, "h1")

    def test_unordered_list(self):
        md = "- Item 1\n- Item 2"
        html_node = markdown_to_html_node(md)
        html = html_node.to_html()
        self.assertIn("<ul>", html)
        self.assertIn("<li>", html)
        self.assertIn("Item 1", html)

    def test_ordered_list(self):
        md = "1. First\n2. Second"
        html_node = markdown_to_html_node(md)
        html = html_node.to_html()
        self.assertIn("<ol>", html)
        self.assertIn("<li>", html)
        self.assertIn("First", html)

    def test_code_block(self):
        md = "```\nCode\n```"
        html_node = markdown_to_html_node(md)
        html = html_node.to_html()
        self.assertIn("<pre><code>", html)  # or <pre><code> if that's how it's generated
        self.assertIn("Code", html)


class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_heading(self):
        md = "# Title"
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div><h1>Title</h1></div>")

    def test_paragraph(self):
        md = "This is a paragraph."
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div><p>This is a paragraph.</p></div>")

    def test_quote(self):
        md = "> A quote\n> still in quote"
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div><blockquote>A quote\nstill in quote</blockquote></div>")

    def test_unordered_list(self):
        md = "- Item one\n- Item two"
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div><ul><li>Item one</li><li>Item two</li></ul></div>")

    def test_ordered_list(self):
        md = "1. First\n2. Second"
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div><ol><li>First</li><li>Second</li></ol></div>")

    def test_code_block(self):
        md = "```\nprint(\"Hello\")\n```"
        html_node = markdown_to_html_node(md)
        self.assertEqual(
            html_node.to_html(),
            "<div><pre><code>print(\"Hello\")</code></pre></div>"
        )

    def test_mixed_content(self):
        md = "# Header\n\nParagraph\n\n- Item 1\n- Item 2"
        html_node = markdown_to_html_node(md)
        self.assertEqual(
            html_node.to_html(),
            "<div><h1>Header</h1><p>Paragraph</p><ul><li>Item 1</li><li>Item 2</li></ul></div>"
        )

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here    
    
    This is another paragraph with _italic_ text and `code` here
    
    
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

if __name__ == '__main__':
    unittest.main()

    
    




