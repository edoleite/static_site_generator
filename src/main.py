from textnode import *
from htmlnode import *
from functions import *

def main():
    #dummy_textnode = TextNode("text", TextType.LINK, "https://www.boot.dev"  )
    #print(repr(dummy_textnode))

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

    print(list_of_block_types)

main()


