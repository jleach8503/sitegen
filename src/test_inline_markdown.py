import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        with self.assertRaises(ValueError) as e:
            nodes = [
                TextNode("This is a text node", TextType.TEXT),
            ]
            split_nodes_delimiter(nodes, "", TextType.TEXT)
        self.assertIn("a delimiter must be provided", str(e.exception))

    def test_invalid_type(self):
        with self.assertRaises(ValueError) as e:
            nodes = [
                TextNode("This is a text node", TextType.TEXT),
            ]
            split_nodes_delimiter(nodes, "*", "superduper")
        self.assertIn("invalid text_type: superduper", str(e.exception))

    def test_non_text_type(self):
        nodes = [
            TextNode("This is a bold node", TextType.BOLD),
            TextNode("This is an italic node", TextType.ITALIC),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is a bold node", TextType.BOLD),
                TextNode("This is an italic node", TextType.ITALIC),
            ]
        )

    def test_bold_type(self):
        nodes = [
            TextNode("This is text with a **bold** word", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_bold_type_complex(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = [
            TextNode(text, TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT),
            ]
        )

    def test_italic_type(self):
        nodes = [
            TextNode("_All text is italics!_", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("All text is italics!", TextType.ITALIC),
            ]
        )

    def test_italic_type_complex(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = [
            TextNode(text, TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is **text** with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT),
            ]
        )

    def test_code_type(self):
        nodes = [
            TextNode("PowerShell cmdlet: `Get-ChildItem`", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("PowerShell cmdlet: ", TextType.TEXT),
                TextNode("Get-ChildItem", TextType.CODE),
            ]
        )

    def test_code_type_complex(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = [
            TextNode(text, TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is **text** with an _italic_ word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT),
            ]
        )


class TestSplitNodesImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_only_text(self):
        node = TextNode(
            "This text doesn't have a single image in the entire thing!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This text doesn't have a single image in the entire thing!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_only_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This ![crap](https://not.real.picture/empty.png) doesn't even exist!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This ", TextType.TEXT),
                TextNode("crap", TextType.IMAGE, "https://not.real.picture/empty.png"),
                TextNode(" doesn't even exist!", TextType.TEXT),
            ],
            new_nodes,
        )


class TestSplitNodesLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_link_only_text(self):
        node = TextNode(
            "This text doesn't have a single link in the entire thing!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This text doesn't have a single link in the entire thing!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_only_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes(self):
        node1 = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This link to [some fake website](https://not.real.website) is so broken!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode("This link to ", TextType.TEXT),
                TextNode("some fake website", TextType.LINK, "https://not.real.website"),
                TextNode(" is so broken!", TextType.TEXT),
            ],
            new_nodes,
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_text_to_textnode(self):
        text = "This has **multiple** links [to youtube](https://www.youtube.com/@bootdotdev) with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and another [link](https://boot.dev). _Hope this works!_"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("multiple", TextType.BOLD),
                TextNode(" links ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" with an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(". ", TextType.TEXT),
                TextNode("Hope this works!", TextType.ITALIC),
            ]
        )


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            matches,
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            matches,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_no_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with absolutely no images!"
        )
        self.assertListEqual(
            matches,
            [],
        )

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to google](https://www.google.com)"
        )
        self.assertListEqual(
            matches,
            [
                ("to google", "https://www.google.com"),
            ],
        )

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            matches,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_extract_no_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with absolutely no links!"
        )
        self.assertListEqual(
            matches,
            [],
        )

class TestMarkdownToBlocks(unittest.TestCase):
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

    def test_markdown_to_blocks_excessive_newlines(self):
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