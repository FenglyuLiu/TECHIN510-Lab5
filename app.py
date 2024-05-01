import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
from db import Database
import requests
import openai
import psycopg2


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_content(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"


def generate_fairytale_image(description):
    try:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=description,
            size="1024x1024",
            quality="standard",
            n=1
        )
        if response.status_code == 200:
            image_url = response['data'][0]['url']
            return image_url
        else:
            image_url = "https://drive.google.com/file/d/166hH2hHF1kDpa5ZwzvJ3UYyntBni-l6s/view?usp=sharing"
            return image_url
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

database_url = os.getenv('DATABASE_URL')
db = Database(database_url)


def generate_fairy_tale(user_request):
    prompt_template = """
    You are an expert at telling fairytales. You are Hans Christian Andersen.

    Please take the users request and write a fairytale for them.

    Please include the following details:
    - Think about the social context of the story. Especially, according to the time of the story.
    - The main character that will be in the story. What's his/her name, interests and personalities.
    - The challenges that will be faced and why is it challenging.
    - The actions that will be taken, this will relate to the main character's characteristics.
    - The result of the story and its impact for the character and the world.

    The user's request is:
    {user_request}
    """

    # 将用户请求插入模板
    complete_prompt = prompt_template.format(user_request=user_request)
    
    # 调用AI模型生成内容
    generated_story = generate_content(complete_prompt)  # 调用之前定义的函数

    return generated_story

# Setup sidebar and main area
with st.sidebar:
    st.header("🐠 Create Your Fairy Tale")
    when = st.text_input("🕒 When did it happen?")
    where = st.text_input("🌏 Where did it happen?")
    character = st.text_input("🤵 Who is the main character?")
    what_happened = st.text_input("📷 What happened?")
    generate_button = st.button("Generate Fairy Tale")

if generate_button:
    prompt = f"When: {when}, Where: {where}, Character: {character}, Event: {what_happened}"
    story_generated = generate_fairy_tale(prompt)
    if story_generated:
        st.header("👀 Generated Fairy Tale")
        st.write(story_generated)
        image_url = generate_fairytale_image(story_generated[:100])  # Use the first 100 characters for image generation
        if image_url is None:
            st.warning("Failed to generate image. Saving the story without an image.")
        
        # Save the story and the image URL to the database, even if image_url is None
        db.insert_fairy_tale(prompt, story_generated, image_url)


        if image_url:
            st.image(image_url, caption="Visual Representation of the Story")


# Display saved and new fairy tales with images
database_url = os.getenv('DATABASE_URL')
with Database(database_url) as db:
    db.create_table()
    df = db.fetch_fairy_tales()
    if df:  # This checks if the list is not empty
        st.header("🎏 Fairy Tales")
        for row in df:
            with st.expander(f"Story {row[0]} - {row[1]}"):
                st.text_area("", value=row[2], height=300, key=f"ta{row[0]}")
                if row[3]:
                    st.image(row[3], caption="Image related to the story")
        else:
            print("No fairy tales found.")
