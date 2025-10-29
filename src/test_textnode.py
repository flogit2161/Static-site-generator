import unittest

from textnode import TextNode, TextType
from functions.text_node_to_html_node import text_node_to_html_node
from functions.split_nodes_delimiter import split_nodes_delimiter
from functions.extract_markdown_regex import extract_markdown_images, extract_markdown_links
from functions.split_images_and_links import split_nodes_images, split_nodes_links
from functions.text_to_textnodes import text_to_textnodes
from functions.markdown_to_blocks import markdown_to_blocks


class TestTextNode(unittest.TestCase):
    # TextNode tests
    def test_eqTrue(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_eq2False(self):
        node = TextNode("This is a link", TextType.LINK, "http://example.com")
        node2 = TextNode("This is not a link", TextType.IMAGE, "http://example.com")
        self.assertNotEqual(node, node2)

    def test_eq3True(self):
        node = TextNode("This is a text node", TextType.ITALIC, "http://example.com")
        node2 = TextNode("This is a text node", TextType.ITALIC, "http://example.com")
        self.assertEqual(node, node2)
    
    
    


    #TextNode to HTMLNode conversion tests
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        bold_node = text_node_to_html_node(node)
        self.assertEqual(bold_node.tag, "b")
        self.assertEqual(bold_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        italic_node = text_node_to_html_node(node)
        self.assertEqual(italic_node.tag, "i")
        self.assertEqual(italic_node.value, "This is an italic text node")

    def test_code(self):
        node = TextNode("print('Hello, World!')", TextType.CODE)
        code_node = text_node_to_html_node(node)
        self.assertEqual(code_node.tag, "code")
        self.assertEqual(code_node.value, "print('Hello, World!')")

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, "http://example.com")
        link_node = text_node_to_html_node(node)
        self.assertEqual(link_node.tag, "a")
        self.assertEqual(link_node.value, "Click here")
        self.assertEqual(link_node.props, {"href": "http://example.com"})

    def test_image(self):
        node = TextNode("An image", TextType.IMAGE, "http://example.com/image.png")
        image_node = text_node_to_html_node(node)
        self.assertEqual(image_node.tag, "img")
        self.assertEqual(image_node.value, "")
        self.assertEqual(image_node.props, {"src": "http://example.com/image.png", "alt": "An image"})
        


   
   
   
    # Split Nodes Delimiter tests
    def test_split_nodes_basic_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))


    def test_split_nodes_basic_italic(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_split_nodes_basic_code(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))
        
    def test_split_nodes_multiple_and_empty(self):
        node = TextNode("This is **bold** and this is _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" and this is ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("italic", TextType.ITALIC))
        

    def test_split_nodes_no_delimiter(self):
        node = TextNode("This is normal text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)




#Extract functions tests

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a text with a link [example](http://example.com)"
        )
        self.assertListEqual([("example", "http://example.com")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with two images ![img1](http://img1.com) and ![img2](http://img2.com)"
        )
        self.assertListEqual(
            [("img1", "http://img1.com"), ("img2", "http://img2.com")],
            matches,
        )

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with two links [link1](http://link1.com) and [link2](http://link2.com)"
        )
        self.assertListEqual(
            [("link1", "http://link1.com"), ("link2", "http://link2.com")],
            matches,
        )


#Split Images from Markdown tests
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_only_image(self):
        node = TextNode(
            "![only image](https://i.imgur.com/onlyimage.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("only image", TextType.IMAGE, "https://i.imgur.com/onlyimage.png"),
            ],
            new_nodes,
        )

    def test_split_image_empty_string(self):
        node = TextNode(
            ''"![image](https://i.imgur.com/emptystring.png)"'',
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/emptystring.png"),
            ],
            new_nodes,
        )
    
    def test_split_no_image(self):
        node = TextNode(
            "This is text without images.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                node,
            ],
            new_nodes,
        )

#Split Links from Markdown tests
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](http://example.com) and another [second link](http://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "http://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "http://example.org"),
            ],
            new_nodes,
        )

    def test_split_only_link(self):
        node = TextNode(
            "[only link](http://onlylink.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("only link", TextType.LINK, "http://onlylink.com"),
            ],
            new_nodes,
        )

    def test_split_link_empty_string(self):
        node = TextNode(
            ''"[link](http://emptystring.com)"'',
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "http://emptystring.com"),
            ],
            new_nodes,
        )

    def test_split_no_link(self):
        node = TextNode(
            "This is text without links.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                node,
            ],
            new_nodes,
        )



#Text to TextNodes tests
    def test_text_to_textnodes(self):
        text = "This is **bold** text with an ![image](http://image.com) and a [link](http://link.com) and `code`."
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "http://image.com"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://link.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected_nodes)


    def test_text_to_textnodes_double_formatting(self):
        text = "This is **bold** and *italic* text."
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected_nodes)


    def test_text_to_textnodes_image_link(self):
        text = "Here is an ![image](http://image.com) and a [link](http://link.com)."
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("Here is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "http://image.com"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://link.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected_nodes)






if __name__ == "__main__":
    unittest.main()