import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

genai.configure(api_key=api_key)

def main():
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("What is life")
        print(response.text)
    except Exception as e:
        print(e)

main()
