import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyDstwHoc3J3vHi3GBq9Vak-g7qhfwP5nYQ")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("")
print(response.text)