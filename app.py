import streamlit as st
from openai import OpenAI

# Load API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Macdini AI – Data Analytics Tutor", page_icon="🧠")

st.title("🧠 Macdini AI – Data Analytics Tutor")
st.write("Ask me anything about Python, SQL, statistics, visualization, cloud, or machine learning.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# OpenAI call (CORRECT FORMAT)
def call_macdini(chat_history):
    return client.responses.create(
        model="gpt-4.1-mini",
        messages=chat_history,
        max_output_tokens=400
    ).output_text

# Display chat messages
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).markdown(msg["content"])

# User input
prompt = st.chat_input("Ask Macdini anything...")

if prompt:
    # Add user's message
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Get assistant reply
    reply = call_macdini(st.session_state.chat_history)

    # Add reply
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

    # Display reply
    st.chat_message("assistant").markdown(reply)
