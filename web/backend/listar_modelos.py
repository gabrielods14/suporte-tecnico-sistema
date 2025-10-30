"""Lista modelos disponíveis do Gemini"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega a chave
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
env_path = os.path.join(backend_dir, '.env')
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("Listando modelos disponíveis...")
print()

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")

