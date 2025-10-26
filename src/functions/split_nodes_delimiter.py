from textnode import TextNode, TextType



# Split Delimiter for Nodes ( Example: Bold / Italic / Code )
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter in node.text:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("Unmatched delimiter in text")
            for i in range(len(parts)):
                if parts[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(parts[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(parts[i], text_type))
        else:
            new_nodes.append(node)
    return new_nodes
