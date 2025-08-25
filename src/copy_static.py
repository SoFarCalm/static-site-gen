import os
import shutil

def copy_static_files(src: str, dest: str):
    if os.path.exists(dest):
        shutil.rmtree(dest)
        os.mkdir(dest)
    else:
        os.mkdir(dest)

    src_dir = os.listdir(src)
    
    for item in src_dir:
        item_src = os.path.join(src, item)
        item_dest = os.path.join(dest, item)
        if os.path.isfile(item_src):
            shutil.copy(item_src, item_dest)
        
    for item in src_dir:
        item_src = os.path.join(src, item)
        item_dest = os.path.join(dest, item)
        if os.path.isdir(item_src):
            copy_static_files(item_src, item_dest)
