import streamlit as st 
from openai import OpenAI

st.set_page_config(page_title="My AI Chatbox")
st.title("My AI Chatbox")

myclient=OpenAI(
    
    base_url='http://localhost:11434/v1/',
    api_key='ollama',
)

def get_completion(prompt):
    
    model="Eomer/gpt-3.5-turbo"
    
    messages=[{"role":"user","content":prompt}]
    
    response=myclient.chat.completions.create(
        
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content



with st.form('my_form'):

   prompt=st.text_area("Enter the prompt")
   text=st.text_area('Enter the question',"Enter the question here")
   submit=st.form_submit_button("submit")
   
if submit and text is not None:
       
       response=get_completion(prompt+"/"+text)
       st.write(response)