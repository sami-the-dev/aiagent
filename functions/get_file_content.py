import os
from config import FILE__CHARS_LIMIT
def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory,file_path)
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(full_path)
    common_path = os.path.commonpath([full_path,working_directory])
    if working_directory != common_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(full_path,"r") as f:
            content = f.read(FILE__CHARS_LIMIT)
            file_size = os.path.getsize(full_path)
            if file_size > FILE__CHARS_LIMIT:
                content += f"{file_path} truncated at 10000 characters"
            return content
    except FileNotFoundError:
        return f"File Not Found"
    except PermissionError:
        return "You do not have the right to do this"
    except Exception as e:
        return f"Error {e}"
