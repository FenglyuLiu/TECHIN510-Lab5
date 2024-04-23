import os

import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

prompt_template = """
You are an expert at telling fairytales.

Please take the users request and write a fairytale for them.

Please include the following details:
- The background of the story
- The main charater that will be in the story
- The challenges that will be faced
- The actions that will be taken
- The result of the story

The user's request is:
{prompt}
"""

def generate_content(prompt):
    response = model.generate_content(prompt)
    return response.text

st.title("🎏 AI Fairy Tale")

prompt = st.text_area("Enter your fairytale request (background, characters, challenges, actions, result, etc.):")
if st.button("Give me a Fairy Tale!"):
    reply = generate_content(prompt)
    st.write(reply)