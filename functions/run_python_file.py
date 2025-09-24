import os
import subprocess
def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.abspath(os.path.join(working_directory,file_path))
    working_directory = os.path.abspath(working_directory)
    common_path = os.path.commonpath([full_path,working_directory])

    if common_path != working_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(file_path):
        return f'Error: File "{file_path}" not found.'
    _,extension =  os.path.splitext(file_path)
    if extension != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    try:
        command = ["python3", full_path] + args
        completed_process = subprocess.run(command,
                                        capture_output=True,
                                        timeout=30,
                                        text=True
                                        )
        stdout = completed_process.stdout
        stderr = completed_process.stderr
        exit_code = completed_process.returncode
        
        # Format the output nicely
        output_parts = []
        if stdout:
            output_parts.append(f"STDOUT:\n{stdout}")
        if stderr:
            output_parts.append(f"STDERR:\n{stderr}")
        if exit_code != 0:
            output_parts.append(f"Process exited with code {exit_code}")
        
        if not output_parts:
            return "No output produced"
        
        return "\n".join(output_parts)
        
    except Exception as e:
        return f"Error: executing Python file: {e}"