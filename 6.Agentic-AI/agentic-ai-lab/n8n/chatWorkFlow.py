import streamlit as st
import requests

# Put your real n8n webhook URL here
webhook_url = st.text_input(
    "Enter your n8n Webhook URL",
    placeholder="",
)
st.title("Demo: Chat with n8n Workflow")

# 1. Ask user to type a message
user_message = st.chat_input("Type your message")

# 2. When user sends a message
if user_message:
    # Show what the user typed
    st.write("You:", user_message)

    # Send the message to n8n
    response = requests.post(
        webhook_url,
        json={"message": user_message},  # sends JSON to your webhook [web:23][web:29]
    )

    # 3. Show what n8n sent back
    # If your webhook returns text
    st.write("n8n says:", response.text)
