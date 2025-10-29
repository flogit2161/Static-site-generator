from htmlnode import HTMLNode, LeafNode, ParentNode
from blocktype import BlockType
from functions.markdown_to_blocks import markdown_to_blocks
from functions.text_node_to_html_node import text_node_to_html_node
from functions.block_to_block_type import block_to_block_type
from functions.text_to_textnodes import text_to_textnodes








def markdown_to_html_node(markdown):
    split_blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in split_blocks:
        block_type = block_to_block_type(block)

        #HEADING BLOCK
        if block_type == BlockType.HEADING:
            heading_node = build_heading(block)
            html_nodes.append(heading_node)

        #QUOTE BLOCK
        elif block_type == BlockType.QUOTE:
            quote_node = build_quote(block)
            html_nodes.append(quote_node)

        #CODE BLOCK
        elif block_type == BlockType.CODE:
            lines = block.splitlines(True) # Keep line endings / could use split("\n")          
            inner = "".join(lines[1:-1])             
            code_leaf = LeafNode(tag="code", value=inner)
            code_node = ParentNode(tag="pre", children=[code_leaf])
            html_nodes.append(code_node)

        #UNORDERED LIST BLOCK
        elif block_type == BlockType.UNORDERED_LIST:
            unordered_node = build_unordered_list(block)
            html_nodes.append(unordered_node)

        #ORDERED LIST BLOCK
        elif block_type == BlockType.ORDERED_LIST:
            ordered_node = build_ordered_list(block)
            html_nodes.append(ordered_node)

        #PARAGRAPH BLOCK
        else:
            lines = block.split("\n")
            paragraph = " ".join(lines)
            children = text_to_children(paragraph)
            paragraph_node = ParentNode(tag="p", children=children)
            html_nodes.append(paragraph_node)

    # Wrap whole thing in a html div
    return ParentNode(tag="div", children=html_nodes)



#HELPER FUNCTIONS

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def build_heading(block):
    i = 0
    while i < len(block) and block[i] == "#":
        i += 1
    count = i
    if not (1 <= count <= 6 and i < len(block) and block[i] == " "):
        raise ValueError("invalid heading block")
    text = block[i+1:].strip()
    children = text_to_children(text)
    return ParentNode(tag=f"h{count}", children=children)

def build_quote(block):
    lines = block.splitlines()
    new_lines = []
    for line in lines:
        if line.startswith(">"):
            new_lines.append(line[1:].strip())
        else:
            new_lines.append(line.strip())
    combined_text = "\n".join(new_lines)
    children = text_to_children(combined_text)
    return ParentNode(tag="blockquote", children=children)

def build_unordered_list(block):
    lines = block.splitlines()
    list_items = []
    for line in lines:
        if line.startswith("- "):
            item_text = line[2:].strip()
            item_children = text_to_children(item_text)
            item_node = ParentNode(tag="li", children=item_children)
            list_items.append(item_node)
        else:
            raise ValueError("invalid unordered list item")
    return ParentNode(tag="ul", children=list_items)
    
def build_ordered_list(block):
    lines = block.splitlines()
    list_items = []
    expected_number = 1
    for line in lines:
        prefix = f"{expected_number}. "
        if line.startswith(prefix):
            item_text = line[len(prefix):].strip()
            item_children = text_to_children(item_text)
            item_node = ParentNode(tag="li", children=item_children)
            list_items.append(item_node)
            expected_number += 1
        else:
            raise ValueError("invalid ordered list item")
    return ParentNode(tag="ol", children=list_items)



    