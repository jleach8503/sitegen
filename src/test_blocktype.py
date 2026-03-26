import unittest

from blocktype import BlockType, is_ordered_list_block, block_to_block_type

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