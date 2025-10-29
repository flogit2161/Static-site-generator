from functions.assets_to_public import assets_to_public
from functions.generate_pages_recursive import generate_pages_recursive
import sys

def main(basepath="/"):
    assets_to_public()
    generate_pages_recursive("content", "template.html", "docs", basepath)
    
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    main(basepath)  