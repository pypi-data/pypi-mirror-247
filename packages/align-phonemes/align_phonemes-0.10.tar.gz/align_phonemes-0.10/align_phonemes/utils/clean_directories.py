import os
import shutil

def clean_directories(dirs):
    for dir in dirs:
        if os.path.exists(dir):
            shutil.rmtree(dir)