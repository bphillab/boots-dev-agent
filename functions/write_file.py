import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs,file_path))
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_file:
        return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    if os.path.isdir(target_file):
        return(f'Error: Cannot write to "{file_path}" as it is a directory')

    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, 'w') as file:
        file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes contents to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="working directory of file to write contents to",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path relative to working directory for file to write contents to",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="contents to be written to file",
            ),
        },
    ),
)

