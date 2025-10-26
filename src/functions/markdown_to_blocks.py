def markdown_to_blocks(markdown):
    blocks = []
    split_lines = markdown.split("\n\n")
    for block in split_lines:
        block = block.strip()
        if block == "":
            continue
        blocks.append(block)
    return blocks
