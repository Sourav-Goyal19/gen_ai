import os
import json
import requests
import platform
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv();

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")

client = genai.Client();

def get_platform():
    os_type = platform.system()
    return os_type

def run_command(command: str):
    print("🔦 Tool called:", command)
    exit_code = os.system(command)
    if exit_code == 0:
        return "✅ Success"
    else:
        return f"❌ Failure with exit code {exit_code}"
    
def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url);
    
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}";
    else:
        return "Something went wrong";

available_tools = {
    "run_command": {
        "fn" : run_command,
        "description": "Takes the command as a parameter, executes the command and return either the success or (failure with error message)."
    },
    "get_platform": {
        "fn": get_platform,
        "description": "Return the operating system name like windows or linux"
    },
    "get_weather": {
        "fn" : get_weather,
        "description": "Takes the city name as a parameter and returns the weather for that city"
    }
}

system_prompt = """
    You are a terminal assistant whose name is 'Terminus' and who knows each command of a platform.
    You help your user by understanding their need and then perform the appropriate command task.
    You will have access to the user's terminal, so try to use that.
    You respond to user queries using step-by-step reasoning: start, plan, action, observe, and result. Output the results in JSON format.
    You perform one step at a time.
    Try to provide a better response to the user query by using the appropriate tool(s) that you have, according to the user query.
    Use your tools to interact with the user's device using commands.
    
    Output JSON format:
    {{
        "step": string,
        "content"?: string,
        "function"?: string,
        "input"?: string,
    }}

    Available Tools to you are:
    - run_command : "Takes the command as a parameter, executes the command and returns either the success or (failure with error message)."
    - get_platform : "Returns the operating system name like windows or linux or mac"
    - get_weather : "Takes the city name as a parameter and returns the current weather for that city"
    
    Rules:
    - Output must be in JSON format
    - Take the action one at a time and wait for the next input
    - Understand the user query carefully
    - When writing code or multi-line content to files, avoid using escape characters like \\n
    - Break multi-line content into multiple echo statements using proper redirection
    - Use '>' for the first line and '>>' for all following lines
    - On Windows, use echo and >> to append lines
    - On Linux/macOS, use echo -e or heredoc if needed
    - Avoid wrapping code in quotes unless absolutely necessary
    - Perform one step at a time

    Example:
    Input: May you create the add.py file and write the function of adding two numbers into that.
    Output: {{ "step": "plan", "content": "The user wants to create a Python file named add.py and write a function that adds two numbers into it." }}
    Output: {{ "step": "plan", "content": "To do this, I need to know the platform because file writing commands vary between Windows and Linux." }}
    Output: {{ "step": "action", "function": "get_platform" }}
    Output: {{ "step": "observe", "content": "Received 'windows'" }}
    Output: {{ "step": "plan", "content": "On Windows, I will use echo to write the function to the file line by line." }}
    Output: {{ "step": "action", "function": "run_command", "input": "echo def add(x, y): > add.py" }}
    Output: {{ "step": "observe", "content": "Received 'Success'" }}
    Output: {{ "step": "action", "function": "run_command", "input": "echo \\treturn x + y >> add.py" }}
    Output: {{ "step": "observe", "content": "Received 'Success'" }}
    Output: {{ "step": "result", "content": "add.py file created successfully with the add function." }}
    
    Input: Hello
    Output: {{ "step": "plan", "content": "user is saying 'hello' which is a greeting. I should also give some greeting." }}
    Output: {{"step": "action", "content" : "Hey! 😊 How's it going? What's on your mind today?"}}
    Output: {{ "step" : "observe", "content" : "Nice reply, according to user input." }}
    Output: {{ "step" : "result", "content": "Hey! 😊 How's it going? What's on your mind today?" }}
"""

chat_config = types.GenerateContentConfig(
    system_instruction=system_prompt,
    response_mime_type="application/json"
)

chat = client.chats.create(
    model="gemini-1.5-flash",
    config=chat_config
)


while True:
    user_input = input(">>");
    
    if user_input == "bye":
        break;
    
    query = [user_input];
    
    while True:
        response = chat.send_message(query);
        query.append(response.text);
        response = json.loads(response.text);
        print(f"🧠 {response}");
        
        
        if response.get("step") == "action":
            #Tool calling part
            tool_name = response.get("function")
            tool_input = response.get("input")
            
            if tool_name in available_tools:
                if tool_input:
                    tool_res = available_tools[tool_name]["fn"](tool_input)
                else:
                    tool_res = available_tools[tool_name]["fn"]()
                print("Tool response:", tool_res);
                query.append(json.dumps({ "step": "observe", "output": tool_res }))
                continue;
        elif response.get("step") == "result":
            print(f"🤖 {response}")
            break;