import google.generativeai as genai
import os
import config

# Use the key from config
os.environ['GEMINI_API_KEY'] = config.Config.GEMINI_API_KEY
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- Name: {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
