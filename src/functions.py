from textnode import *
from htmlnode import *
import re

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

#this function extracts images from MD texts
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

#this function extracts normal links from MD texts
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

#this function creates new textnodes from old ones for image types
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # Text olmayan node'ları olduğu gibi ekle
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Text boşsa, işlemeyeceğiz ama önce tüm listeye bakmamız lazım
        if not node.text.strip():
            continue  # ama hemen eklemiyoruz, aşağıda duruma göre karar verilecek

        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        pos = 0
        text = node.text
        for alt_text, url in matches:
            pattern = f"![{alt_text}]({url})"
            idx = text.find(pattern, pos)
            if idx == -1:
                continue

            before = text[pos:idx]
            if before.strip():
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            pos = idx + len(pattern)

        after = text[pos:]
        if after.strip():
            new_nodes.append(TextNode(after, TextType.TEXT))

    # Eğer hiçbir yeni node üretilmediyse ve orijinal liste sadece boş bir TEXT node'undan oluşuyorsa
    if not new_nodes and len(old_nodes) == 1 and old_nodes[0].text_type == TextType.TEXT and not old_nodes[0].text.strip():
        return old_nodes

    return new_nodes

#this function creates new text nodes from old ones for link types
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # Text olmayan node'ları olduğu gibi ekle
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Text boşsa, işlemeyeceğiz ama önce tüm listeye bakmamız lazım
        if not node.text.strip():
            continue  # ama hemen eklemiyoruz, aşağıda duruma göre karar verilecek

        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        pos = 0
        text = node.text
        for link, url in matches:
            pattern = f"[{link}]({url})"
            idx = text.find(pattern, pos)
            if idx == -1:
                continue

            before = text[pos:idx]
            if before.strip():
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(link, TextType.LINK, url))
            pos = idx + len(pattern)

        after = text[pos:]
        if after.strip():
            new_nodes.append(TextNode(after, TextType.TEXT))

    # Eğer hiçbir yeni node üretilmediyse ve orijinal liste sadece boş bir TEXT node'undan oluşuyorsa
    if not new_nodes and len(old_nodes) == 1 and old_nodes[0].text_type == TextType.TEXT and not old_nodes[0].text.strip():
        return old_nodes

    return new_nodes

def text_to_textnodes(text):
   markdown_syntax = {
        TextType.BOLD: "**",
        TextType.ITALIC: "_",
        TextType.CODE:  "`"
    }

   text_node = TextNode(text, TextType.TEXT)
   text_nodes = split_nodes_image([text_node])
   text_nodes = split_nodes_link(text_nodes)
   
   for k, v in markdown_syntax.items():
       text_nodes = split_nodes_delimiter(text_nodes, v, k)
   return text_nodes








