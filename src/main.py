from textnode import *

def main():
    dummy_textnode = TextNode("text", TextType.LINK, "https://www.boot.dev"  )
    print(repr(dummy_textnode))

main()