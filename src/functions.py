from textnode import *
from htmlnode import *

#this function turn a text node to a html node (leafnode more specifically)
def text_node_to_html_node(text_node):       
    
    if text_node.text_type == TextType.TEXT:
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

#this function creates textnodes from raw markdown strings
def split_nodes_delimiter(old_nodes, delimiter, text_type):    
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # TextType.TEXT olmayanlar olduğu gibi kalsın
            new_nodes.append(node)
        else:
            if delimiter not in node.text:
                # Delimiter yoksa hata fırlatabilirsin ya da node'yu olduğu gibi ekle
                #raise Exception(f"Delimiter '{delimiter}' not found in text: {node.text}")
                # veya bu satırı kullan:
                new_nodes.append(node)
            else:
                parts = node.text.split(delimiter)
                if len(parts) < 3:
                    raise Exception(f"Text does not have delimiter '{delimiter}' in correct positions: {node.text}")
                
                # parts: ['This is ', 'italic', ' and this is ', 'also italic', ' text']
                # yani tek seferde 3 parçaya bölmek yetmez

                # Burada şunu yapabiliriz:
                # parts içindeki tek sayılı indexleri text_type ile, çift sayılı indexleri TextType.TEXT ile dönüştürelim
                
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        # çift index => normal text
                        if part:
                            new_nodes.append(TextNode(part, TextType.TEXT))
                    else:
                        # tek index => belirtilen text_type
                        new_nodes.append(TextNode(part, text_type))
    return new_nodes

