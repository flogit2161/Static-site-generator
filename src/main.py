from functions.assets_to_public import assets_to_public
from functions.generate_pages_recursive import generate_pages_recursive

def main():
    assets_to_public()
    generate_pages_recursive("content", "template.html", "public")
    
    

if __name__ == "__main__":
    main()  