import os
import json
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv();

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")

client = genai.Client();

def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url);
    
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}";
    else:
        return "Something went wrong";

available_tools = {
    "get_weather": {
        "fn" : get_weather,
        "description": "Takes the city name as a parameter and returns the weather for that city"
    }
}

system_prompt = """
    You are a helpful assistant that helps user to resolve their queries.
    
    You respond user query by start, plan, action, observe and result. Output the results in json format.
    You perform one step at a time.
    You try to provide the better response of the user query by using the appropriate tool(s) that you have, according to user query.
    
    Output JSON format:
    {{
        "step": string,
        "content"?: string,
        "function"?: string,
        "input"?: string,
    }}
    
    Available Tools to you are:
    - get_weather : "Takes the city name as a parameter and returns the current weather for that city"
    
    Rules:
    Output must be in json format
    Take the action one at a time and wait for the next input.
    Understand the user query carefully.
    
    Example:
    Input: What is the current weather in new york city?
    Output: {{ "step": "plan", "content": "Alright, user is asking about the current weather of the new work city." }}
    Output: {{ "step": "plan", "content": "Right now, I don't have the current time and updates. So I have to check the available tools for fetching the real time weather }}
    Output: {{ "step": "plan", "content": "From the available tools list, get_weather is looking appropriate for this task. So let's use it. }},
    Output: {{ "step": "action", "function": "get_weather", "input" : "new york" }}
    Output: {{ "step": "observe", "output" : "12 degree celcius" }}
    Output: {{ "step" : "result", "content" : "The current weather for the new york city is 12 degree C." }}
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
                tool_res = available_tools[tool_name].get("fn")(tool_input);
                query.append(json.dumps({ "step": "observe", "output": tool_res }))
                continue;
        elif response.get("step") == "result":
            print(f"🤖 {response}")
            break;    