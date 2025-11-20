import streamlit as st
from openai import OpenAI

# Use the key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# System prompt for Macdini
SYSTEM_PROMPT = """
You are Macdini AI, a patient and friendly Data Analytics tutor.
You explain Python, SQL, statistics, data visualization, cloud, and machine learning
in simple language with clear examples.
"""

# Streamlit page setup
st.set_page_config(page_title="Macdini AI – Data Analytics Tutor", page_icon="🧠")
st.title("🧠 Macdini AI – Data Analytics Tutor")
st.write("Ask me anything about Python, SQL, statistics, visualization, cloud, or machine learning.")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---- OpenAI call using CHAT COMPLETIONS (correct) ----
def call_macdini(chat_history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        max_tokens=400
    )

    return completion.choices[0].message.content

# Show chat history in UI
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).markdown(msg["content"])

# User input
user_input = st.chat_input("Ask Macdini anything...")

if user_input:
    # Save user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Get reply from OpenAI
    reply = call_macdini(st.session_state.chat_history)

    # Save assistant reply
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

    # Display reply
    st.chat_message("assistant").markdown(reply)
