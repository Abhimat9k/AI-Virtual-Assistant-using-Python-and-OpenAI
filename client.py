from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    api_key = os.getenv('API_KEY'),
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks just like Alexa and Google Cloud."},
        {
            "role": "user",
            "content": "What is programming."
        }
    ]
)

print(completion.choices[0].message)