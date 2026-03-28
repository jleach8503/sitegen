import os
import shutil
from markdown_blocks import markdown_to_html_node, extract_title


BASE_DIR = os.path.dirname(os.path.split(os.path.abspath(__file__))[0])
STATIC_DIR = os.path.join(BASE_DIR, "static")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
CONTENT_DIR = os.path.join(BASE_DIR, "content")

def copy_asset(source, destination, clean=False):
    if clean and os.path.exists(destination):
        shutil.rmtree(destination)
        os.mkdir(destination)

    for name in os.listdir(source):
        source_path = os.path.join(source, name)
        target_path = os.path.join(destination, name)

        if os.path.isfile(source_path):
            shutil.copy(source_path, target_path)
            continue

        if not os.path.exists(target_path):
            os.mkdir(target_path)
        copy_asset(source_path, target_path, False)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    content = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(content)
    


def main():
    copy_asset(STATIC_DIR, PUBLIC_DIR, True)
    generate_page(
        os.path.join(CONTENT_DIR, "index.md"),
        os.path.join(BASE_DIR, "template.html"),
        os.path.join(PUBLIC_DIR, "index.html")
    )


if __name__ == "__main__":
    main()