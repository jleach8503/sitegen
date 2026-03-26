from textnode import TextNode, TextType
from extractors import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter is None or len(delimiter) == 0:
        raise ValueError("a delimiter must be provided")
    if not isinstance(text_type, TextType):
        raise ValueError(f"invalid text_type: {text_type}")
    
    split_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            split_nodes.append(node)
            continue
        
        split_lines = node.text.split(delimiter)
        if len(split_lines) % 2 != 1:
            raise ValueError(f"invalid markdown - missing closing delimiter: {node.text}")
        for index in range(len(split_lines)):
            if split_lines[index] == "":
                continue
            if index % 2 == 0:
                split_nodes.append(TextNode(split_lines[index], TextType.TEXT))
            else:
                split_nodes.append(TextNode(split_lines[index], text_type))

    return split_nodes


def split_nodes_image(old_nodes):
    split_nodes = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            split_nodes.append(node)
            continue

        remaining_text = node.text
        for image in images:
            before, remaining_text = remaining_text.split(f"![{image[0]}]({image[1]})", 1)
            if before != "":
                split_nodes.append(TextNode(before, TextType.TEXT))
            split_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

        if remaining_text != "":
                split_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return split_nodes


def split_nodes_link(old_nodes):
    split_nodes = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            split_nodes.append(node)
            continue

        remaining_text = node.text
        for link in links:
            before, remaining_text = remaining_text.split(f"[{link[0]}]({link[1]})", 1)
            if before != "":
                split_nodes.append(TextNode(before, TextType.TEXT))
            split_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

        if remaining_text != "":
                split_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return split_nodes


def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)

    return text_nodes