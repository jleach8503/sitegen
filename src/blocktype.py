import re
from enum import Enum

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