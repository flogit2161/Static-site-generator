from functions.markdown_to_html_node import markdown_to_html_node
from functions.extract_title import extract_title
import os

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        src_path_content = f.read()
    with open(template_path, "r") as f1:
        template_content = f1.read()
    from_path_to_html = markdown_to_html_node(src_path_content)
    content = from_path_to_html.to_html()
    title = extract_title(src_path_content)
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", content)
    if not basepath.endswith("/"):
        basepath += "/"
    final_html = final_html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path:
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as f3:
        f3.write(final_html)
        

    
