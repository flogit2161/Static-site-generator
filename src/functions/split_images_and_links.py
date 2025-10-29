from textnode import TextNode, TextType
from .extract_markdown_regex import extract_markdown_images, extract_markdown_links




#Split image markdown from Text
def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        image = extract_markdown_images(node.text)
        if not image:
            new_nodes.append(node)  
            continue
        #AI Code from here 
        after = node.text
        for alt, url in image:
            snippet = f"![{alt}]({url})"
            before, after = after.split(snippet, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
        if after:
            new_nodes.append(TextNode(after, TextType.TEXT))
    return new_nodes
        
#Split links markdown from Text
def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        #Same AI Code
        after = node.text
        for link_text, url in links:
            snippet = f"[{link_text}]({url})"
            before, after = after.split(snippet, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
        if after:
            new_nodes.append(TextNode(after, TextType.TEXT))
    return new_nodes