import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
from db import Database

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def generate_content(prompt):
    # This function will send the prompt to the AI model and return the generated text
    try:
        response = model.generate_content(prompt)
        return response.text  # Assuming the response object has a text attribute containing the generated text
    except Exception as e:
        return f"An error occurred: {e}"

    
def generate_fairy_tale(user_request):
    prompt_template = """
    You are an expert at telling fairytales.

    Please take the users request and write a fairytale for them.

    Please include the following details:
    - The background of the story
    - The main character that will be in the story
    - The challenges that will be faced
    - The actions that will be taken
    - The result of the story

    The user's request is:
    {user_request}
    """

    # 将用户请求插入模板
    complete_prompt = prompt_template.format(user_request=user_request)
    
    # 调用AI模型生成内容
    generated_story = generate_content(complete_prompt)  # 调用之前定义的函数

    return generated_story



st.title("🎏 AI Fairy Tale")

prompt = st.text_area("Enter your fairytale request (background, characters, challenges, actions, result, etc.):")

if st.button("Generate Fairy Tale"):
    reply = generate_fairy_tale(prompt)
    if reply:
        st.write(reply)
        database_url = os.getenv('DATABASE_URL')
        db = Database(database_url)
        with db:
            db.create_table()
            db.insert_fairy_tale(prompt, reply)
            st.success("Fairy tale saved successfully!")

# Always display the fairy tales from the database
database_url = os.getenv('DATABASE_URL')
db = Database(database_url)
with db:
    df = db.fetch_fairy_tales()
    if not df.empty:
        # Styling for the cards
        st.markdown("""
        <style>
        .card {
            margin: 10px;
            padding: 10px;
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
            transition: 0.3s;
            border-radius: 5px; /* 5px rounded corners */
        }
        </style>
        """, unsafe_allow_html=True)

        # Display the cards
        for index, row in df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="card">
                <h3>{row['prompt']}</h3>
                <p>{row['fairy_tale']}</p>
                </div>
                """, unsafe_allow_html=True)

