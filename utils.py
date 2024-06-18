"""
Util classes
"""

import shutil


def save_file_to_directory(uploaded_file) -> str:
    """
    save a file to directory
    """
    # path to save
    path = f"./static/user_audios/{uploaded_file.filename}"
    with open(path, "w+b") as file:
        shutil.copyfileobj(uploaded_file.file, file)

    return path
