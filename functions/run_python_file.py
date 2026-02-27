import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs,file_path))
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_file:
        return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(target_file):
        return(f'Error: "{file_path}" does not exist or is not a regular file')
    if not target_file.endswith('.py'):
        return(f'Error: "{file_path}" is not a Python file')
    command = ["python", target_file]
    command.extend(args or [])
    x = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=30)
    returncode = x.returncode
    stdout = x.stdout
    stderr = x.stderr
    retstr = ""
    if returncode != 0:
        retstr += f"Process exited with code {returncode}\n"
    if not stdout and not stderr:
        retstr += "No output produced\n"
    else:
        retstr += "STDOUT:" + stdout + "\n"
        retstr += "STDERR:" + stderr + "\n"
    return retstr


schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Runs a python file with given args",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "working_directory": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to the python file",
                ),
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="path to the file relative to working directory. File is a run python file",
                ),
                "args": types.Schema(
                    type=types.Type.STRING,
                    description="arguments to be passed to python file",
                ),
            },
        ),
    )


