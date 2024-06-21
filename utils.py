"""
Util classes
"""

import shutil


def save_file_to_directory(uploaded_file, directory) -> str:
    """
    save a file to directory
    """
    # path to save
    path = f"./static/{directory}/{uploaded_file.filename}"
    with open(path, "w+b") as file:
        shutil.copyfileobj(uploaded_file.file, file)

    return path
