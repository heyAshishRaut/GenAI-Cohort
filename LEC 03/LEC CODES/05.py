import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
import platform
import subprocess

load_dotenv()

client = OpenAI()

def run_command(command):
    result = os.system(command=command)
    return result

def get_weather(city: str):
    print("Tools called - ", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"

def add(x, y):
    print("Tools called - add ")

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "That takes a city name as input and return current weather for the city"
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input and execute on system and return output"
    }
}

system_prompt = """
    You are a helpful AI assitant who is specialised in resolving userr query.
    You work on START, PLAN, ACTION, OBSERVE mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select relevant tool from available tools. And based on tool selection you perform and action to call the tool.
    Wait for observation and based on observation from tool call resolve user query.

    Rule -
    - Follow the Output JSON Format
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query
    - Just use WINDOWS command and not LINUX

    Output JSON Format: 
    {{
        "step":"string",
        "content":"string",
        "function":"The name of function if step is action",
        "input": "The input parameter for the function"
    }}

    Available Tools:
    - get_weather: Takes a city name as an input and returns the current weather for the city
    - run_command: Takes a command as input to execute on system and return output

    Example -
    User Query: What is weather of new york?
    Output: {{"step": "plan", "content": "User is interested in weather data of new york"}}
    Output: {{"step": "plan", "content": "from the available tools i should call get_weather"}}
    Output: {{"step": "action", "content": "User is interested in weather data of new york"}}
    Output: {{"step": "output", "content": "The weather of new york seems to be 12 Degree"}}

"""
messages = [
    {"role": "system", "content": system_prompt}
]

while True:
    user_query = input(' - ')
    messages.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format = {"type": "json_object"},
            messages = messages
        )
        parsedOutput = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsedOutput)})

        if parsedOutput.get("step") == "plan":
            print(f" > {parsedOutput.get("content")}")
            continue

        if parsedOutput.get("step") == "action":
            tool_name = parsedOutput.get("function")
            tool_input = parsedOutput.get("input")

            if available_tools.get(tool_name, False) != False:
                output = available_tools[tool_name].get("fn")(tool_input)
                messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                continue

        if parsedOutput.get("step") == "output":
            print(f" - {parsedOutput.get("content")}")
            break
