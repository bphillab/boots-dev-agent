import os
from google.genai import types
from config import CHARS_TO_READ

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs,file_path))
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_file:
        return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(target_file):
        return(f'Error: File not found or is not a regular file: "{file_path}"')
    with open(target_file, 'r') as file:
        content = file.read(CHARS_TO_READ)
        if file.read(1):
            content += f'[...File "{file_path}" truncated at {CHARS_TO_READ} characters]'
    return content

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets contents of a file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to file",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to file to read contents",
            ),
        },
    ),
)




