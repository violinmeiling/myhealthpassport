import google.generativeai as genai
import os

genai.configure(api_key="")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("")
print(response.text)
