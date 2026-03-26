import re


def extract_markdown_images(text):
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return [(found[0], found[1]) for found in re.findall(regex, text)]


def extract_markdown_links(text):
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return [(found[0], found[1]) for found in re.findall(regex, text)]