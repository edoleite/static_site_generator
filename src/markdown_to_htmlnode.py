from functions import *
import re


def markdown_to_html_node(md):
    
    md_blocks = markdown_to_blocks(md)    
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
