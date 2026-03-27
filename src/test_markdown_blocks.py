import unittest

from htmlnode import LeafNode
from markdown_blocks import (
    BlockType,
    is_ordered_list_block,
    block_to_block_type,
    text_to_children,
)

class TestIsOrderedListBlock(unittest.TestCase):
    def test_valid_ordered_list(self):
        block = (
            "1. First item\n"
            "2. Second item\n"
            "3. Third item"
        )
        self.assertTrue(is_ordered_list_block(block))

    def test_invalid_missing_space(self):
        block = (
            "1.First item\n"
            "2. Second item"
        )
        self.assertFalse(is_ordered_list_block(block))

    def test_invalid_wrong_start_number(self):
        block = (
            "2. First item\n"
            "3. Second item"
        )
        self.assertFalse(is_ordered_list_block(block))

    def test_invalid_non_incrementing(self):
        block = (
            "1. First item\n"
            "3. Third item"
        )
        self.assertFalse(is_ordered_list_block(block))

    def test_invalid_mixed_content(self):
        block = (
            "1. First item\n"
            "Not a list line\n"
            "3. Third item"
        )
        self.assertFalse(is_ordered_list_block(block))


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_block(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> Another line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph_block(self):
        block = "This is just a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_unordered_list(self):
        block = "-item one\n- item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_ordered_list(self):
        block = "1. first\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestTextToChildren(unittest.TestCase):
    def test_single_child_plain_text(self):
        text = "hello"
        children = text_to_children(text)

        self.assertListEqual(
            children,
            [LeafNode(None, "hello")]
        )

    def test_multiple_children_bold_and_plain(self):
        text = "hello **world**"
        children = text_to_children(text)

        self.assertListEqual(
            children,
            [
                LeafNode(None, "hello "),
                LeafNode("b", "world"),
            ]
        )

    def test_multiple_children_mixed_formatting(self):
        text = "This is _italic_ and **bold** and `code`."
        children = text_to_children(text)

        self.assertListEqual(
            children,
            [
                LeafNode(None, "This is "),
                LeafNode("i", "italic"),
                LeafNode(None, " and "),
                LeafNode("b", "bold"),
                LeafNode(None, " and "),
                LeafNode("code", "code"),
                LeafNode(None, "."),
            ]
        )

    def test_empty_string_returns_empty_list(self):
        text = ""
        children = text_to_children(text)

        self.assertEqual(children, [])

    def test_image_node(self):
        text = "Look at this ![alt text](image.png)"
        children = text_to_children(text)

        self.assertListEqual(
            children,
            [
                LeafNode(None, "Look at this "),
                LeafNode("img", "", {"src": "image.png", "alt": "alt text"}),
            ]
        )

    def test_link_node(self):
        text = "Click [here](https://example.com)"
        children = text_to_children(text)

        self.assertListEqual(
            children,
            [
                LeafNode(None, "Click "),
                LeafNode("a", "here", {"href": "https://example.com"}),
            ]
        )