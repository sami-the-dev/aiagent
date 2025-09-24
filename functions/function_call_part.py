import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.genai import types
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from calculator.get_files_info import get_files_info

def call_function(function_call_part, verbose=False):
    # Print function call info
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    # Function mapping
    functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }
    
    function_name = function_call_part.name
    
    # Check if function exists
    if function_name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Prepare arguments with working_directory
    args = dict(function_call_part.args) if function_call_part.args else {}
    args["working_directory"] = "./calculator"
    
    try:
        # Call the function
        function_result = functions[function_name](**args)
        
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error calling {function_name}: {str(e)}"},
                )
            ],
        )