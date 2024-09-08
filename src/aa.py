import os
from dotenv import load_dotenv


load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

print(google_api_key)
print(openai_api_key)