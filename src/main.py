from textnode import *
from htmlnode import *

def main():
    dummy_textnode = TextNode("text", TextType.LINK, "https://www.boot.dev"  )
    print(repr(dummy_textnode))

main()


def text_node_to_html_node(text_node):       
    
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(tag=None, value=text_node.text)
    
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", value=None, props={"href": text_node.url})
    
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", value="", props={"src": text_node.url, "alt": text_node.text})
    
    raise Exception("invalid text type")