from textnode import *
from htmlnode import *
from functions import *
from markdown_to_htmlnode import *

def main():
    md = """# Heading One

This is a paragraph.

## Heading Two

> This is a quote.
> Still in the quote.

- Item one
- Item two
- Item three

1. First
2. Second
3. Third

"""
    html_node = markdown_to_html_node(md)
    print(html_node.to_html())


main()


