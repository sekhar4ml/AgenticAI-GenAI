import openai
import streamlit as st
from streamlit_chat import message
import os 
from dotenv import load_dotenv
load_dotenv('api_key.env')
openai.api_key = os.environ.get('YOUR SECRET KEY')
def generate_response(prompt):
    completion=openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.6,
    )
    message=completion.choices[0].text
    return message