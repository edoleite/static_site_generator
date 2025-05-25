from htmlnode import LeafNode
from textnode import TextNode, TextType
from functions import split_nodes_delimiter  # doğru modülü kullan

# Giriş: TextNode listesi, bazıları "*italic*" gibi markdown içeriyor
nodes = [
    TextNode("This is *italic* text", TextType.TEXT),
    TextNode("This is normal", TextType.TEXT),
    TextNode("Code should not *change*", TextType.CODE),
]

# '*' karakterine göre split edip, ortadaki parçayı ITALIC olarak işaretliyoruz
try:
    result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)

    for r in result:
        print(f"text: {r.text}, type: {r.text_type}")
except Exception as e:
    print(f"Error: {e}")
