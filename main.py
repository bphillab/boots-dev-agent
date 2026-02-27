
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
import argparse


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Now we can access `args.user_prompt`
    for _ in range(10):
        resps = response_loop(client, messages, args)
        messages.append(types.Content(role="user", parts=[types.Part(text=resps)]))
        if _ == 19:
            print("Reached maximum number of iterations. Exiting.")
            sys.exit(1)


def response_loop(client, messages,args):
    resp = client.models.generate_content(
        contents=messages,
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0,
            tools=[available_functions]
        )
    )
    new_message = f"Candidates considered: \n"
    for candidate in resp.candidates:
        new_message += f"{candidate.content}\n"

    if args.verbose:
        print("User prompt:", args.user_prompt)
        print("Prompt tokens:", resp.usage_metadata.prompt_token_count)
        print("Response tokens:", resp.usage_metadata.candidates_token_count)
    if resp.text:
        print(resp.text)
    if resp.function_calls:
        responses = []
        for function_call in resp.function_calls:
            function_call_result = call_function(function_call, args.verbose)
            if not function_call_result.parts:
                raise ValueError("Function call parts is empty")
            func_resp = function_call_result.parts[0].function_response
            if not func_resp:
                raise ValueError("Function call response is empty")
            responses.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        for response in responses:
            new_message += f"-> {response.function_response.response}\n"
    return new_message

if __name__ == "__main__":
    main()
