from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        
    raise ValueError(f"invalid text_type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter is None or len(delimiter) == 0:
        raise ValueError("a delimiter must be provided")
    if not isinstance(text_type, TextType):
        raise ValueError(f"invalid text_type: {text_type}")
    
    split_nodes = []
    if len(old_nodes) == 0:
        return split_nodes
    
    if len(old_nodes) > 1:
        for node in old_nodes:
            split_nodes.extend(split_nodes_delimiter([node], delimiter, text_type))
        return split_nodes

    node = old_nodes[0]
    if node.text_type is not TextType.TEXT:
        split_nodes.append(node)
        return split_nodes
    
    split_lines = node.text.split(delimiter)
    if len(split_lines) != 3:
        raise ValueError(f"invalid markdown - missing closing delimiter: {node.text}")
    for index in range(len(split_lines)):
        if split_lines[index] == "":
            continue
        if index % 2 == 0:
            split_nodes.append(TextNode(split_lines[index], TextType.TEXT))
        else:
            split_nodes.append(TextNode(split_lines[index], text_type))

    return split_nodes