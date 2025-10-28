from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    i = 0 
    while i < len(block) and block[i] == '#':
        i += 1
    count = i
    if 1 <= count <= 6 and i < len(block) and block[i] == ' ':
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    split_block = block.splitlines()

    for line in split_block:
        if not line.startswith(">"):
            return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    for line in split_block:
        if not line.startswith("- "):
            return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
        
    expected_number = 1    
    for line in split_block:
        if not line.startswith(f"{expected_number}. "):
            return BlockType.PARAGRAPH
        expected_number += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    
