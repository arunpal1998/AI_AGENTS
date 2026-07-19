from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('google_api_key')

client = genai.Client(api_key = api_key)

while True:
    question = input('Ask anything:')

    if question.lower() == 'exit':
        break

    response = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents = question
    )

    print('AI:',response.text)