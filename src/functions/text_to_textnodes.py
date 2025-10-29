from textnode import TextNode, TextType
from .split_images_and_links import split_nodes_images, split_nodes_links
from .split_nodes_delimiter import split_nodes_delimiter


def text_to_textnodes(text):
    text = TextNode(text, TextType.TEXT)
    text = split_nodes_images([text])
    text = split_nodes_links(text)
    text = split_nodes_delimiter(text, "**", TextType.BOLD)
    text = split_nodes_delimiter(text, "*", TextType.ITALIC)
    text = split_nodes_delimiter(text, "_", TextType.ITALIC)
    text = split_nodes_delimiter(text, "`", TextType.CODE)
    return text
