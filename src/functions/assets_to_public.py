import os 
import shutil

def assets_to_public():
    destination = "docs"
    source = "assets"
    if os.path.exists(destination):
        shutil.rmtree(destination)
        print(f"Removed existing '{destination}' directory.")
    os.mkdir(destination)
    print(f"Created new '{destination}' directory.")
    helper_copy(source, destination)
    

def helper_copy(source, destination):
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        if os.path.isdir(source_path):
            if not os.path.exists(destination_path):
                os.mkdir(destination_path)
                print(f"Creating directory: {destination_path}")
            helper_copy(source_path, destination_path)
            print(f"Copied directory: {source_path} to {destination_path}")
        else:
            shutil.copy(source_path, destination_path) 
            print(f"Copied file: {source_path} to {destination_path}")


