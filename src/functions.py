from textnode import *
from htmlnode import *
from blocknode import BlockType
import re
import os
import shutil

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

def markdown_to_blocks(markdown):
    blocks = re.split(r'\n\s*\n', markdown)  # splits on empty lines, even with spaces
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH
   
#markdown to html node fonksiyonlari
def markdown_to_html_node(md):
    
    md_blocks = markdown_to_blocks(md)

    for i, block in enumerate(md_blocks):
        block_type = block_to_block_type(block)
    
        # If paragraph, join lines with spaces
        if block_type == BlockType.PARAGRAPH:
            block = " ".join(line.strip() for line in block.splitlines())
            md_blocks[i] = block
    
    block_nodes = []

    for block in md_blocks:
        
        block_type = block_to_block_type(block)
        
        tag = determine_tag(block)
        block = remove_marker(block)
        
        if block_type != BlockType.CODE:
            childrens = text_to_children(block, block_type)
            block_node = ParentNode(tag, flatten_children(childrens))
            block_nodes.append(block_node)
        else:
            innermost_node = TextNode(block, TextType.CODE)
            code_node = text_node_to_html_node(innermost_node)           
            pre_node = ParentNode("pre", [code_node])
            block_nodes.append(pre_node)      
    
    res_node = ParentNode("div", block_nodes)
    return res_node

def determine_tag(block):
    block_type = block_to_block_type(block)
    tag_map = {
        BlockType.PARAGRAPH: "p",
        BlockType.QUOTE: "blockquote",
        BlockType.CODE : "code",    
        BlockType.ULIST : "ul",
        BlockType.OLIST : "ol",
        BlockType.HEADING: ["h1", "h2", "h3", "h4", "h5", "h6"]
    }
    
    if block_type == BlockType.HEADING:
        hashes = [char for char in block if char == "#"]
        tag = tag_map[BlockType.HEADING][len(hashes)-1]
    else:
        tag = tag_map[block_type]

    return tag
   
def remove_marker(block):
    block_type = block_to_block_type(block)
    
    if block_type == BlockType.QUOTE:
        lines = block.split("\n")
        stripped_lines = []
        for line in lines:
            if line.startswith(">"):
                first_strip = line.lstrip(">")
                second_strip = first_strip.strip()
                stripped_lines.append(second_strip)
            else:
                stripped_lines.append(line)

        new_block = "\n".join(stripped_lines)
        return new_block
    
    if block_type == BlockType.HEADING:
        split_index = 0
        for i in range(len(block)):
           if block[i] == "#":
               split_index = i + 1
           else:
               break
                          
        return block[split_index:].strip()    
    
    if block_type == BlockType.ULIST or block_type == BlockType.OLIST:
        lines = block.split("\n")
        stripped_lines = []
        for line in lines:                        
            stripped_line = re.sub(r'^(- |\d+\. )', '', line)
            double_stripped_line = stripped_line.strip()
            stripped_lines.append(double_stripped_line)
        
        new_block = "\n".join(stripped_lines)        
        return new_block
    
    if block_type == BlockType.CODE:
        lines = block.split("\n")

        if lines[0] == "```":
            del lines[0]
        if lines[-1] == "```":
            del lines[-1]

        first_index = 0
        last_index = 0

        for i in range(len(lines)):
            if lines[i].strip():
                continue
            else:
                first_index = i
                break
            
        for i in range(len(lines)-1, -1, -1):
            if lines[i].strip():
                last_index = i
                break            
            else:
                continue
                

        return "\n".join(lines[first_index: last_index +1 ])

    return block

def text_to_children(block, block_type):

    children_nodes = []   

    if block_type in [BlockType.ULIST, BlockType.OLIST]:
        lines = block.split("\n")        
        for line in lines:               
            lines_text_nodes = text_to_textnodes(line)
            lines_html_nodes = [text_node_to_html_node(node) for node in lines_text_nodes]                
            lines_parent_node = ParentNode("li", lines_html_nodes)
            children_nodes.append(lines_parent_node) 
        
    else:
        text_nodes = text_to_textnodes(block)
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
        children_nodes.extend(html_nodes)         

    return children_nodes

def flatten_children(children):
    flat = []

    for child in children:
        if isinstance(child, list):
            flat.extend(flatten_children(child))  # Recursive flattening
        else:
            if not hasattr(child, "to_html") or not callable(child.to_html):
                raise TypeError(f"Child {child} is not a valid node (missing to_html())")
            flat.append(child)
    
    return flat

#md to html node sonu

#copy static fuctions

def clean_content(path):
        if os.path.exists(path):
            contents = os.listdir(path)
            for item in contents:
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif not os.listdir(item_path):
                    os.rmdir(item_path)
                else:
                    clean_content(item_path)
        else:
            raise Exception("path does not exist")

def copy_contents(source, destination):
    #clean destination folder
    if os.path.exists(destination):
        clean_content(destination)
    
    if os.path.exists(source):
        contents = os.listdir(source)
        if contents:
            for item in contents:
                item_src = os.path.join(source, item)
                item_dest = os.path.join(destination, item)

                if os.path.isfile(item_src):
                    print(f"copying file {item_src} to {item_dest}")
                    os.makedirs(os.path.dirname(item_dest), exist_ok=True)
                    shutil.copy(item_src, item_dest)
                elif os.listdir(item_src):
                    copy_contents(item_src, item_dest)
                else:
                    os.makedirs(item_dest)
        else:
            raise Exception("source directory is empty")
    
                



