import os


def get_files_info(working_directory, directory="."):
    full_dir = os.path.join(working_directory, directory)
    full_dir = os.path.abspath(full_dir)  # Normalize to absolute path
    working_directory = os.path.abspath(working_directory)  # Normalize to absolute path
    
    # Check if the requested directory is within the working directory
    try:
        common_path = os.path.commonpath([full_dir, working_directory])
        if common_path != working_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except ValueError:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_dir):
        return f'Error: "{directory}" is not a directory'
    
    try:
        contents = os.listdir(full_dir)
        result = "Result for current directory:"
        for d in contents:
            current_path = os.path.join(full_dir,d)
            is_dir = os.path.isdir(current_path)
            total_file_size = 0
            if is_dir:
                for dirpath,dirnames,filenames in os.walk(current_path):
                    for file_name in filenames:
                        file_path = os.path.join(dirpath,file_name)
                        try:
                            file_size = os.path.getsize(file_path)
                            total_file_size += file_size
                        except OSError:
                            pass
            else:
                total_file_size += os.path.getsize(current_path)
            
            result+= f"\n - {d}: file_size={total_file_size} bytes, is_dir={is_dir}"
        
        return result
                    

           
    except FileNotFoundError:
        return f"Directory Not Found"
    except PermissionError:
        return f"you do not have the permissions to do that"

