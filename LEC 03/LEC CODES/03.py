import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def get_weather(city: str):
    return "32 Degree celcius"

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

    Output JSON Format: 
    {{
        "step":"string",
        "content":"string",
        "function":"The name of function if step is action",
        "input": "The input parameter for the function"
    }}

    Example -
    User Query: What is weather of new york?
    Output: {{"step": "plan", "content": "User is interested in weather data of new york"}}
    Output: {{"step": "plan", "content": "from the available tools i should call get_weather"}}
    Output: {{"step": "action", "content": "User is interested in weather data of new york"}}
    Output: {{"step": "output", "content": "The weather of new york seems to be 12 Degree"}}

"""

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_format = {"type": "json_object"},
    messages=[
        {"role": "system", "content": system_prompt},
        {"role" : "user", "content": "What is the current weather of Nagpur?"},
        {"role": "assistant", "content": json.dumps({"step": "plan", "content": "User is asking for the current weather of Nagpur"})},
        {"role": "assistant", "content": json.dumps({"step": "plan", "content": "from the available tools I should call get_weather"})},
        {"role": "assistant", "content": json.dumps({"step": "action", "content": "User is asking for the current weather of Nagpur", "function": "get_weather", "input": "Nagpur"})},
        {"role": "assistant", "content": json.dumps({"step": "observe", "output": "32 degree celcius"})}
    ]
)

print(response.choices[0].message.content)