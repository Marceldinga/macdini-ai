import streamlit as st
from openai import OpenAI

# Initialize client (reads OPENAI_API_KEY from environment)
client = OpenAI()

MACDINI_SYSTEM_PROMPT = """
You are Macdini AI, a patient and friendly Data Analytics tutor created by Marcel Dinga.

Your job:
- Teach Python for data (pandas, NumPy, basic matplotlib),
- Teach SQL (SELECT, WHERE, GROUP BY, HAVING, JOIN, ORDER BY, LIMIT),
- Teach statistics for data analysis (mean, median, variance, standard deviation, correlation, distributions, probability basics, confidence intervals in simple terms),
- Teach data visualization (bar charts, histograms, box plots, scatter plots, line charts; when to use each and how to interpret them),
- Introduce basic machine learning for analytics (train/test split, regression, classification, overfitting vs. underfitting, evaluation metrics like accuracy, precision/recall, RMSE in simple language).

Teaching style:
- Always start from the user's current level: explain concepts in simple language, then go deeper if they ask.
- Use small, concrete examples using Python or SQL.
- When explaining code, explain line by line.
- Encourage learning by doing: frequently give small practice questions or exercises and ask the user to try.
- When the user shows code or an answer, give clear feedback: what is correct, what is wrong, and how to fix it.
- Avoid unnecessary jargon. If you use a technical term, briefly define it.
- Be supportive and motivating. Never make the user feel bad for not knowing something.

Constraints:
- If you don't know something or it is outside data analytics/programming, say so briefly.
- If the user requests “single code”, provide one complete runnable block.
"""

st.set_page_config(page_title="Macdini AI – Data Analytics Tutor", page_icon="🧠")
st.title("🧠 Macdini AI – Data Analytics Tutor")
st.write("Ask me anything about Python, SQL, statistics, visualization, or machine learning for data analytics.")

# Store message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": MACDINI_SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hello! I am Macdini AI, your data analytics tutor. How can I help you today?"}
    ]

# Display history
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
prompt = st.chat_input("Ask Macdini anything…")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Macdini is thinking..."):
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=st.session_state.messages
            )
            answer = response.output[0].content[0].text
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
