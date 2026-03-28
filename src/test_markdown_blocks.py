import unittest

from htmlnode import ParentNode, LeafNode
from markdown_blocks import (
    BlockType,
    is_ordered_list_block,
    block_to_block_type,
    text_to_children,
    heading_block_to_html_node,
    paragraph_block_to_html_node,
    code_block_to_html_node,
    quote_block_to_html_node,
    list_block_to_html_node,
    markdown_to_html_node,
    extract_title,
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
            [LeafNode(None, "hello")],
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


class TestHeadingBlockToHtmlNode(unittest.TestCase):
    def test_h1_heading(self):
        block = "# Hello world"
        node = heading_block_to_html_node(block)

        self.assertEqual(node.tag, "h1")
        self.assertEqual(
            node.children,
            [LeafNode(None, "Hello world")],
        )

    def test_h3_heading(self):
        block = "### This is a test"
        node = heading_block_to_html_node(block)

        self.assertEqual(node.tag, "h3")
        self.assertEqual(
            node.children,
            [LeafNode(None, "This is a test")],
        )

    def test_heading_with_inline_formatting(self):
        block = "## Hello **world**"
        node = heading_block_to_html_node(block)

        self.assertEqual(node.tag, "h2")
        self.assertEqual(
            node.children,
            [
                LeafNode(None, "Hello "),
                LeafNode("b", "world"),
            ]
        )

    def test_heading_with_italic_and_code(self):
        block = "#### Mix _this_ and `that`"
        node = heading_block_to_html_node(block)

        self.assertEqual(node.tag, "h4")
        self.assertEqual(
            node.children,
            [
                LeafNode(None, "Mix "),
                LeafNode("i", "this"),
                LeafNode(None, " and "),
                LeafNode("code", "that"),
            ]
        )


class TestParagraphBlockToHtmlNode(unittest.TestCase):
    def test_simple_paragraph(self):
        block = "This is a paragraph."
        node = paragraph_block_to_html_node(block)

        self.assertEqual(node.tag, "p")
        self.assertEqual(
            node.children,
            [LeafNode(None, "This is a paragraph.")],
        )

    def test_paragraph_with_newlines(self):
        block = "This is a paragraph\nthat spans multiple lines."
        node = paragraph_block_to_html_node(block)

        self.assertEqual(node.tag, "p")
        self.assertEqual(
            node.children,
            [LeafNode(None, "This is a paragraph that spans multiple lines.")],
        )

    def test_paragraph_with_bold_and_italic(self):
        block = "This is **bold** and _italic_ text."
        node = paragraph_block_to_html_node(block)

        self.assertEqual(node.tag, "p")
        self.assertEqual(
            node.children,
            [
                LeafNode(None, "This is "),
                LeafNode("b", "bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
                LeafNode(None, " text."),
            ]
        )

    def test_paragraph_with_code_and_link(self):
        block = "Use `code` and visit [here](https://example.com)."
        node = paragraph_block_to_html_node(block)

        self.assertEqual(node.tag, "p")
        self.assertEqual(
            node.children,
            [
                LeafNode(None, "Use "),
                LeafNode("code", "code"),
                LeafNode(None, " and visit "),
                LeafNode("a", "here", {"href": "https://example.com"}),
                LeafNode(None, "."),
            ]
        )

    def test_empty_paragraph(self):
        block = ""
        node = paragraph_block_to_html_node(block)

        # Empty string becomes empty children list
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.children, [])


class TestListBlockToHtmlNode(unittest.TestCase):
    def test_unordered_list_simple(self):
        block = "- item one\n- item two"
        node = list_block_to_html_node(block)

        self.assertEqual(node.tag, "ul")
        self.assertEqual(
            node.children,
            [
                ParentNode("li", [LeafNode(None, "item one")]),
                ParentNode("li", [LeafNode(None, "item two")]),
            ]
        )

    def test_unordered_list_with_inline_formatting(self):
        block = "- **bold** text\n- _italic_ text"
        node = list_block_to_html_node(block)

        self.assertEqual(node.tag, "ul")
        self.assertEqual(
            node.children,
            [
                ParentNode("li", [
                    LeafNode("b", "bold"),
                    LeafNode(None, " text"),
                ]),
                ParentNode("li", [
                    LeafNode("i", "italic"),
                    LeafNode(None, " text"),
                ]),
            ]
        )

    def test_ordered_list_simple(self):
        block = "1. first\n2. second\n3. third"
        node = list_block_to_html_node(block)

        self.assertEqual(node.tag, "ol")
        self.assertEqual(
            node.children,
            [
                ParentNode("li", [LeafNode(None, "first")]),
                ParentNode("li", [LeafNode(None, "second")]),
                ParentNode("li", [LeafNode(None, "third")]),
            ]
        )

    def test_ordered_list_with_inline_formatting(self):
        block = "1. **bold**\n2. `code`"
        node = list_block_to_html_node(block)

        self.assertEqual(node.tag, "ol")
        self.assertEqual(
            node.children,
            [
                ParentNode("li", [
                    LeafNode("b", "bold")
                ]),
                ParentNode("li", [
                    LeafNode("code", "code")
                ]),
            ]
        )

    def test_list_items_with_links(self):
        block = "- Visit [here](https://example.com)\n- Or [there](https://example.org)"
        node = list_block_to_html_node(block)

        self.assertEqual(node.tag, "ul")
        self.assertEqual(
            node.children,
            [
                ParentNode("li", [
                    LeafNode(None, "Visit "),
                    LeafNode("a", "here", {"href": "https://example.com"}),
                ]),
                ParentNode("li", [
                    LeafNode(None, "Or "),
                    LeafNode("a", "there", {"href": "https://example.org"}),
                ]),
            ]
        )


class TestQuoteBlockToHtmlNode(unittest.TestCase):
    def test_single_line_quote(self):
        block = "> This is a quote"
        node = quote_block_to_html_node(block)

        self.assertEqual(node.tag, "blockquote")
        self.assertEqual(
            node.children,
            [
                LeafNode(None, "This is a quote"),
            ]
        )

    def test_multi_line_quote(self):
        block = "> This is line one\n> This is line two"
        node = quote_block_to_html_node(block)

        self.assertEqual(node.tag, "blockquote")
        self.assertEqual(
            node.children,
            [
                LeafNode(None, "This is line one This is line two"),
            ]
        )

    def test_quote_with_inline_formatting(self):
        block = "> This is **bold** and _italic_"
        node = quote_block_to_html_node(block)

        self.assertEqual(node.tag, "blockquote")
        self.assertEqual(
            node.children,
            [
                LeafNode(None, "This is "),
                LeafNode("b", "bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
            ]
        )

    def test_quote_with_code_and_link(self):
        block = "> Use `code` and visit [here](https://example.com)"
        node = quote_block_to_html_node(block)

        self.assertEqual(node.tag, "blockquote")
        self.assertEqual(
            node.children,
            [
                LeafNode(None, "Use "),
                LeafNode("code", "code"),
                LeafNode(None, " and visit "),
                LeafNode("a", "here", {"href": "https://example.com"}),
            ]
        )


class TestCodeBlockToHtmlNode(unittest.TestCase):
    def test_simple_code_block(self):
        block = "```\nprint('hello')\n```"
        node = code_block_to_html_node(block)

        self.assertEqual(node.tag, "pre")
        self.assertEqual(
            node.children,
            [
                ParentNode("code", [
                    LeafNode(None, "print('hello')")
                ])
            ]
        )

    def test_multiline_code_block(self):
        block = "```\nline1\nline2\nline3\n```"
        node = code_block_to_html_node(block)

        self.assertEqual(node.tag, "pre")
        self.assertEqual(
            node.children,
            [
                ParentNode("code", [
                    LeafNode(None, "line1\nline2\nline3")
                ])
            ]
        )

    def test_code_block_with_symbols(self):
        block = "```\n<tag> & special chars\n```"
        node = code_block_to_html_node(block)

        self.assertEqual(node.tag, "pre")
        self.assertEqual(
            node.children,
            [
                ParentNode("code", [
                    LeafNode(None, "<tag> & special chars")
                ])
            ]
        )

    def test_code_block_ignores_inline_formatting(self):
        block = "```\n**not bold** and _not italic_\n```"
        node = code_block_to_html_node(block)

        self.assertEqual(node.tag, "pre")
        self.assertEqual(
            node.children,
            [
                ParentNode("code", [
                    LeafNode(None, "**not bold** and _not italic_")
                ])
            ]
        )


class TestMarkdownToHtmlNode(unittest.TestCase):
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
            "<div>"
            "<p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p>"
            "</div>",
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
            "<div>"
            "<pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre>"
            "</div>",
        )

    def test_multiple_blocks(self):
        md = """# Heading

This is a paragraph.

- item one
- item two
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>Heading</h1>"
            "<p>This is a paragraph.</p>"
            "<ul><li>item one</li><li>item two</li></ul>"
            "</div>",
        )

    def test_mixed_markdown(self):
        md = """## Subheading

> quoted text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h2>Subheading</h2>"
            "<blockquote>quoted text</blockquote>"
            "</div>",
        )

    def test_multiple_paragraphs(self):
        md = """First paragraph here.

Second paragraph here.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<p>First paragraph here.</p>"
            "<p>Second paragraph here.</p>"
            "</div>",
        )


class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")

    def test_title_with_whitespace(self):
        md = "#   My Great Title   "
        self.assertEqual(extract_title(md), "My Great Title")

    def test_multiline_markdown(self):
        md = """# Blog Post Title
Some content here.
More content here."""
        self.assertEqual(extract_title(md), "Blog Post Title")

    def test_missing_title_raises(self):
        md = "No title here at all"
        with self.assertRaises(ValueError):
            extract_title(md)
