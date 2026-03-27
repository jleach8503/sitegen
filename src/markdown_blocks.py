import re
from enum import Enum
from htmlnode import ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes, markdown_to_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def is_ordered_list_block(block):
    lines = block.splitlines()

    for index, line in enumerate(lines):
        expected_prefix = f"{index + 1}. "
        if not line.startswith(expected_prefix):
            return False

    return True


def block_to_block_type(block):
    if bool(re.match(r"^(#{1,6}) (.+)$", block)):
        return BlockType.HEADING
    if bool(re.match(r"^```(?:\n)([\s\S]*?)```$", block)):
        return BlockType.CODE
    if bool(re.match(r"^(>\s?.*(\n>\s?.*)*)$", block)):
        return BlockType.QUOTE
    if bool(re.match(r"^-\s.+(\n-\s.+)*$", block)):
        return BlockType.UNORDERED_LIST
    if is_ordered_list_block(block):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


def text_to_children(text):
    children = []

    for node in text_to_textnodes(text):
        children.append(text_node_to_html_node(node))

    return children


def heading_block_to_html_node(block):
    split_block = block.split(" ", maxsplit=1)

    tag = f"h{len(split_block[0])}"
    children = text_to_children(split_block[1])
    
    return ParentNode(tag, children)


def paragraph_block_to_html_node(block):
    new_text = block.replace("\n", " ")
    tag = "p"
    children = text_to_children(new_text)

    return ParentNode(tag, children)


def code_block_to_html_node(block):
    tag = "pre"
    lines = block.splitlines()
    text_node = TextNode("\n".join(lines[1:-1]) + "\n", TextType.TEXT)
    children = [ParentNode("code", [text_node_to_html_node(text_node)])]

    return ParentNode(tag, children)


def quote_block_to_html_node(block):
    tag = "blockquote"
    children = []

    lines = []
    for line in block.splitlines():
        text = line.split(">", maxsplit=1)[1].removeprefix(" ")
        lines.append(text)

    combined_lines = " ".join(lines)
    children.append(ParentNode("p", text_to_children(combined_lines)))

    return ParentNode(tag, children)


def list_block_to_html_node(block):
    if is_ordered_list_block(block):
        tag = "ol"
    else:
        tag = "ul"

    children = []
    for line in block.splitlines():
        text = line.split(" ", maxsplit=1)[1]
        children.append(ParentNode("li", text_to_children(text)))

    return ParentNode(tag, children)


def markdown_to_html_node(markdown):
    children = []

    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                child = paragraph_block_to_html_node(block)
            case BlockType.HEADING:
                child = heading_block_to_html_node(block)
            case BlockType.CODE:
                child = code_block_to_html_node(block)
            case BlockType.QUOTE:
                child = quote_block_to_html_node(block)
            case BlockType.ORDERED_LIST | BlockType.UNORDERED_LIST:
                child = list_block_to_html_node(block)
        children.append(child)

    return ParentNode("div", children)
