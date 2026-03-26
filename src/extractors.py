import re


def extract_markdown_images(text):
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return [(found[0], found[1]) for found in re.findall(regex, text)]


def extract_markdown_links(text):
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return [(found[0], found[1]) for found in re.findall(regex, text)]


def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        stripped = block.strip()
        if len(stripped) > 0:
            blocks.append(stripped)
    return blocks
