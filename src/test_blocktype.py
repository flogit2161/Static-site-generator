import unittest
from blocktype import BlockType
from functions.block_to_block_type import block_to_block_type
from functions.markdown_to_blocks import markdown_to_blocks
from functions.markdown_to_html_node import markdown_to_html_node






class TestMarkdownFunctions(unittest.TestCase):


#Markdown to blocks tests / Careful with identation of tests here
        def test_markdown_to_blocks(self):
                md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
                blocks = markdown_to_blocks(md)
                self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        def test_markdown_to_blocks_empty(self):
                md = "\n\n"
                blocks = markdown_to_blocks(md)
                self.assertEqual(blocks, [])

        def test_markdown_to_ones_single_block(self):
                md = "This is a single block of text without any double newlines."
                blocks = markdown_to_blocks(md)
                self.assertEqual(blocks, ["This is a single block of text without any double newlines."])




# Block to BlockType tests

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



# Markdown to HTMLNode tests
        def test_paragraphs(self):
                md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

                node = markdown_to_html_node(md)
                html = node.to_html()
                self.assertEqual(
                html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

        def test_codeblock(self):
                md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

                node = markdown_to_html_node(md)
                html = node.to_html()
                self.assertEqual(
                html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )


        def test_unordered_list(self):
                md = """
- Item 1
- Item 2 with **bold**
- Item 3 with _italic_
"""
                node = markdown_to_html_node(md)
                html = node.to_html()
                self.assertEqual(
                html,
            "<div><ul><li>Item 1</li><li>Item 2 with <b>bold</b></li><li>Item 3 with <i>italic</i></li></ul></div>",
        )
                
        def test_ordered_list(self):
                md = """
1. First item
2. Second item with `code`
3. Third item
"""
                node = markdown_to_html_node(md)
                html = node.to_html()
                self.assertEqual(
                html,
                "<div><ol><li>First item</li><li>Second item with <code>code</code></li><li>Third item</li></ol></div>",
        )
        
        def test_heading(self):
                md = """
# This is a Heading 1

## This is a Heading 2
"""
                node = markdown_to_html_node(md)
                html = node.to_html()
                self.assertEqual(
                html,
                "<div><h1>This is a Heading 1</h1><h2>This is a Heading 2</h2></div>",
        )