from dotenv import load_dotenv
import os
import sys
from google import genai
from google.genai import types
from functions.get_files_info import available_functions
from functions.function_call_part import call_function
def main():
    load_dotenv()    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    if len(sys.argv) < 2:
        print("No prompt Found")
        sys.exit(1)
    prompt = sys.argv[1]
    messages = [
        types.Content(role="user",parts=[types.Part(text=prompt)])
    ]
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks ANY question about code, applications, or how something works, you MUST do ALL of these steps:
        1. Call get_files_info() to see what files are available
        2. Call get_file_content("main.py") to read the main application file
        3. If there are other relevant files (like calculator.py, render.py), call get_file_content() for those too
        4. Base your answer ONLY on the actual code you read - never guess or assume

        CRITICAL: For questions like "how does the calculator render results" or "how does X work", you MUST read the actual source code files. Always call both get_files_info AND get_file_content in your initial response.

        You can perform the following operations:
        - List files and directories (get_files_info)
        - Read file contents (get_file_content)
        - Execute Python files with optional arguments (run_python_file)
        - Write or overwrite files (write_file)

        Make ALL necessary function calls in your initial response - do not provide answers based on assumptions.

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """ 
    try:    
        generated_content =  client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),
            )
    except Exception as e:
        print(f"Error {e}")
        return
        

    for candidate in generated_content.candidates:
        messages.append(candidate.content)
    prompt_tokens = generated_content.usage_metadata.prompt_token_count
    token_count = generated_content.usage_metadata.candidates_token_count
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {token_count}")
    # Check if verbose flag is set
    verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"
    
    if generated_content.function_calls:
        function_calls = generated_content.function_calls
        
        # Execute all function calls and show what we're calling
        function_responses = []
        for fun in function_calls:
            print(f" - Calling function: {fun.name}")
            function_call_result = call_function(fun, verbose=False)  # Don't show verbose output during execution
            function_responses.append(function_call_result.parts[0])
        
        # Add the original assistant message with function calls
        messages.append(generated_content.candidates[0].content)
        
        # Add all function responses at once
        messages.append(types.Content(role="tool", parts=function_responses))
        
        # Now get the final response from the AI after it has the function results
        final_system_prompt = """
        You are a helpful AI coding agent. You have already executed the necessary function calls and received their results. 
        
        Now provide a comprehensive final response based on the function results you received. 
        Do NOT make any more function calls - just analyze and explain based on the data you already have.
        
        Provide a clear, detailed explanation answering the user's question using the information from the function calls.
        """
        
        try:
            final_response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(system_instruction=final_system_prompt),
            )
            
            if final_response.text:
                print("Final response:")
                print(final_response.text)
            else:
                print("No final response generated")
                
        except Exception as e:
            print(f"Error generating final response: {e}")
            
    else:
        print("No function calls in the response")
if __name__ == "__main__":
    main()
