
import streamlit as st
from openai import OpenAI
import os

# Load API key from Streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Streamlit Page Config
st.set_page_config(page_title="Macdini AI – Data Analytics Tutor", page_icon="🧠")

# Title
st.title("🧠 Macdini AI – Data Analytics Tutor")
st.write("Ask me anything about Python, SQL, statistics, visualization, machine learning, cloud, or data analytics.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to call OpenAI
def call_macdini(messages):
    response = client.responses.create(
        model="gpt-4.1-mini",    # FIXED MODEL
        input=messages,
        max_output_tokens=500
    )

    return response.output_text

# Display chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.chat_message("user").markdown(chat["content"])
    else:
        st.chat_message("assistant").markdown(chat["content"])

# User input
user_input = st.chat_input("Ask Macdini anything...")

if user_input:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Build messages for API
    messages = []
    for m in st.session_state.chat_history:
        messages.append(f"{m['role']}: {m['content']}")

    # Get AI response
    answer = call_macdini(messages)

    # Add assistant response
    st.session_state.chat_history.append({"role": "assistant", "content": answer})

    # Display response
    st.chat_message("assistant").markdown(answer)
