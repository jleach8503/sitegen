import os
import sys
import shutil
from markdown_blocks import markdown_to_html_node, extract_title


BASE_DIR = os.path.dirname(os.path.split(os.path.abspath(__file__))[0])
STATIC_DIR = os.path.join(BASE_DIR, "static")
CONTENT_DIR = os.path.join(BASE_DIR, "content")
OUTPUT_DIR = os.path.join(BASE_DIR, "docs")


def copy_asset(source, destination, clean=False):
    if clean and os.path.exists(destination):
        shutil.rmtree(destination)

    os.makedirs(destination, exist_ok=True)
    for name in os.listdir(source):
        source_path = os.path.join(source, name)
        target_path = os.path.join(destination, name)

        if os.path.isfile(source_path):
            shutil.copy(source_path, target_path)
            continue

        if not os.path.exists(target_path):
            os.mkdir(target_path)
        copy_asset(source_path, target_path, False)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    if not basepath.endswith("/"):
        basepath += "/"
    content = (
        template
            .replace("{{ Title }}", title)
            .replace("{{ Content }}", html)
            .replace('href="/', f'href="{basepath}')
            .replace('src="/',f'src="{basepath}')
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for name in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, name)
        target_path = os.path.join(dest_dir_path, name)

        if os.path.isfile(source_path) and os.path.splitext(source_path)[1] == ".md":
            target_path = os.path.splitext(target_path)[0] + ".html"
            generate_page(source_path, template_path, target_path, basepath)
            continue

        if os.path.isdir(source_path):            
            generate_pages_recursive(source_path, template_path, target_path, basepath)
            continue
    


def main():
    basepath = sys.argv[1] if len(sys.argv[1]) > 1 else "/"    

    copy_asset(STATIC_DIR, OUTPUT_DIR, True)
    generate_pages_recursive(
        CONTENT_DIR,
        os.path.join(BASE_DIR, "template.html"),
        OUTPUT_DIR,
        basepath,
    )


if __name__ == "__main__":
    main()