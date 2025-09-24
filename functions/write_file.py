import os
def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        full_path = os.path.abspath(full_path)
        working_directory = os.path.abspath(working_directory)
        
        # Check if the file is within the working directory
        try:
            common = os.path.commonpath([full_path, working_directory])
            if common != working_directory:
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        except ValueError:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Write the file
        with open(full_path, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {e}"