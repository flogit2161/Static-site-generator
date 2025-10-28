from blocktype import BlockType, block_to_block_type
import unittest


def test_block_to_block_type(self):
    block = "# Heading 1"
    self.assertEqual(block_to_block_type(block), BlockType.HEADING)

def test_block_to_block_type_code(self):
    block = "```\ncode block\n```"
    self.assertEqual(block_to_block_type(block), BlockType.CODE)

def test_block_to_block_type_quote(self):
    block = "> This is a quote.\n> It has multiple lines."
    self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

def test_block_to_block_type_unordered_list(self):
    block = "- Item 1\n- Item 2\n- Item 3"
    self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

def test_block_to_block_type_ordered_list(self):
    block = "1. First item\n2. Second item\n3. Third item"
    self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
