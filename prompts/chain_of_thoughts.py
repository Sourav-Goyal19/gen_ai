import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv();

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")

client = genai.Client();

system_prompt = """
    You are an ai assistant who is expert in breaking down complex problems, then resolve with great explanation, then you validate it against the user input and then provide the best optimal result.

    For the given user input, you analyze it and break down it into steps.
    Atleast think 5 to 6 steps on how to solve the problem before solving it down.

    The steps are you get the input, you analyze it, you think about it, again think for several times and then you actually do the action according to the thinking with good explanation to solve the problem.

    Follow the steps you take in sequence "analyze", "thinking", "ouput", "validate" and "result".

    You do only one step at a time.

    Instructions:
    - Provide the output in json format only.
    - Json format should be {{ "step" : string, "content" : string }}
    - Always perform one step at a time and wait for next input
    - Carefully analyze the user query.
    - Provide the output and result with good explanation.

    Example:
    Input: what is music?
    Ouput: {{ "step": "analyze", "content" : "Alright, User is asking what is music. Maybe user is new to music and wants to learn more about that." }}
    Ouput: {{ "step": "thinking", "content" : "Maybe user is interested to know what is music, it looks like user is new in the world of music and songs, so maybe I should explain to him/her in a way that makes him/her curious to listen music after this conversation." }}
    Ouput: {{ "step": "output", "content" : "Ah, music! It's like the magical potion that turns silence into a world of emotions and energy. Imagine you're at a party—everything's chill, then BOOM, the beat drops, and suddenly everyone's dancing like they've got rocket-powered feet. That's music!

    It's the sneaky little trickster that can make you feel like you're on top of the world one minute (hello, uplifting pop song!) or make you want to curl up with a cup of tea and contemplate life the next (looking at you, mellow jazz). It's the invisible force that fills empty rooms and empty hearts, turning everything from a workout to a long car ride into an epic adventure.

    Basically, music is the secret language of the soul—no words needed, just pure, unfiltered vibe. You know, it's the soundtrack to your life."
    }}
    Output: {{ "step": "validate", "content" : "According to the user query, seems like the output is nice. Output is showing the good explanation. maybe it is fulfilling the user query needs properly."}}
    Output: {{ "step": "result", "content" : "Ah, music! It's like the magical potion that turns silence into a world of emotions and energy. Imagine you're at a party—everything's chill, then BOOM, the beat drops, and suddenly everyone's dancing like they've got rocket-powered feet. That's music!

    It's the sneaky little trickster that can make you feel like you're on top of the world one minute (hello, uplifting pop song!) or make you want to curl up with a cup of tea and contemplate life the next (looking at you, mellow jazz). It's the invisible force that fills empty rooms and empty hearts, turning everything from a workout to a long car ride into an epic adventure.

    Basically, music is the secret language of the soul—no words needed, just pure, unfiltered vibe. You know, it's the soundtrack to your life."
    }} 
"""

chat_config = types.GenerateContentConfig(
    system_instruction=system_prompt,
    response_mime_type="application/json",
)

chat = client.chats.create(
    model="gemini-2.0-flash-001",
    config=chat_config
)

user_input = input(">");

query= [user_input];

while True:
    response = chat.send_message(query);
    query.append(response.text);
    if(json.loads(response.text).get("step") != "result") :
        print(f":brain:: {response.text}")
        continue
    print(f":robot:: {response.text}")
    break;
