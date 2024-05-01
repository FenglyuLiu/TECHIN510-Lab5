# Frontend Development: AI Fairy Tale

## Introduction

AI Fairy Tale is a web application that uses advanced natural language processing to generate fairy tales based on user input. This project is designed to demonstrate the integration of AI capabilities in frontend development, providing a unique storytelling experience.

<img width="738" alt="Screenshot 2024-04-23 at 23 38 47" src="https://github.com/FenglyuLiu/TECHIN510-Lab5/assets/88125716/794e74e1-80c7-4167-98f8-e04feabdf028">

I want the user to have more control over the story, depending on time, characters, events, and so on. I added more detailed explanations to each prompt, which can help LLM generate more layered and detailed stories.

<img width="1507" alt="Screenshot 2024-05-01 at 10 24 21" src="https://github.com/FenglyuLiu/TECHIN510-Lab5-Lab6/assets/88125716/bf209d66-f4fc-4856-a792-8200dbf7be1f">


## Features

- **User Input for Custom Tales**: Users can enter specific details to guide the story generation.
- **AI-Powered Content Creation**: Leveraging a generative AI model to create engaging and coherent fairy tales.
- **Responsive Design**: Compatible with various devices, ensuring a seamless user experience.
- **Persistent Storage**: Integrated database for storing and retrieving generated fairy tales.


## Technologies Used

- **Python**: Primary programming language used for backend development.
- **Streamlit**: An open-source app framework used to create the frontend of the application.
- **Google Generative AI**: AI model from Google used for generating fairy tale content.
- **PostgreSQL**: The relational database used for persistent storage of tales.
- **Supabase**: An open-source Firebase alternative providing the backend services.


## How to Run This Code
Open the terminal and run the following commands:

    python -m venv venv
    
    source venv/bin/activate
    
    pip install -r requirements.txt


## What's included

Within the download you'll find the following directories and files, logically grouping common assets and providing both compiled and minified variations. You'll see something like this:

AI-Fairy-Tale/

├── .env

├── .gitignore

├── app_json_rest_api.py

├── app.py

├── db.py

├── README.md

├── requests_api.py

└── requirements.txt


## What I Learned

- Utilizing Google's Generative AI model for text generation.
- Creating a user-friendly frontend with Streamlit.
- Integrating a PostgreSQL database with a Python application.
