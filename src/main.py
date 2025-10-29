from functions.assets_to_public import assets_to_public
from functions.generate_page import generate_page

def main():
    assets_to_public()
    generate_page("content/index.md", "template.html", "public/index.html")
    

if __name__ == "__main__":
    main()  