import streamlit as st
from openai import OpenAI
import pandas as pd
from io import BytesIO

# Create client (uses OPENAI_API_KEY from Streamlit secrets)
client = OpenAI()

# ---------- BASE SYSTEM PROMPT ----------
BASE_SYSTEM_PROMPT = """
You are Macdini AI, a patient and friendly Data Analytics tutor created by Marcel Dinga.

Your job:
- Teach Python for data (pandas, NumPy, basic matplotlib),
- Teach SQL (SELECT, WHERE, GROUP BY, HAVING, JOIN, ORDER BY, LIMIT),
- Teach statistics (mean, median, variance, standard deviation, correlation, distributions, probability basics),
- Teach data visualization (bar charts, histograms, scatter plots, etc.),
- Teach basic machine learning (train/test split, regression, classification, metrics).

Teaching style:
- Explain concepts in simple language, then go deeper only if asked.
- Use small examples.
- Give practice tasks.
- Encourage the user.
- Define any jargon.

Constraints:
- Stay in the domain of data analytics and programming.
"""

# ---------- STREAMLIT PAGE CONFIG ----------
st.set_page_config(page_title="Macdini AI – Data Analytics Tutor", page_icon="🧠")
st.title("🧠 Macdini AI – Data Analytics Tutor")
st.write("Ask me anything about Python, SQL, statistics, visualization, or machine learning for data analytics.")

# ---------- SESSION STATE ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_notes" not in st.session_state:
    st.session_state.user_notes = ""

if "df" not in st.session_state:
    st.session_state.df = None


# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("Macdini Settings")

    mode = st.selectbox(
        "Choose mode",
        ["Tutor chat", "CSV analysis", "Practice quiz"]
    )

    st.markdown("### Session memory / notes")
    st.session_state.user_notes = st.text_area(
        "Notes:",
        value=st.session_state.user_notes,
        height=120
    )

    st.markdown("---")
    st.markdown("### Voice Input")
    use_voice_input = st.checkbox("Enable audio input (transcription)")


# ---------- HELPER FUNCTIONS ----------
def build_system_prompt(extra_instructions: str = "") -> str:
    prompt = BASE_SYSTEM_PROMPT.strip()

    notes = st.session_state.user_notes.strip()
    if notes:
        prompt += "\n\nExtra session notes from user:\n" + notes

    if extra_instructions:
        prompt += "\n\nTask instructions:\n" + extra_instructions

    return prompt


def call_macdini(messages, extra_instructions: str = "") -> str:
    """Core function to call OpenAI Responses API."""
    system_message = {"role": "system", "content": build_system_prompt(extra_instructions)}

    response = client.responses.create(
        model="gpt-4o-mini",  # FIXED MODEL
        input=[system_message] + messages,
    )

    return response.output[0].content[0].text


def transcribe_audio(uploaded_file) -> str:
    """Convert audio to text."""
    bytes_data = uploaded_file.read()
    audio_io = BytesIO(bytes_data)
    audio_io.name = uploaded_file.name

    transcription = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=audio_io
    )
    return transcription.text


# ---------- MODE 1: TUTOR CHAT ----------
if mode == "Tutor chat":
    st.subheader("💬 Tutor Chat")

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    audio_file = None
    if use_voice_input:
        audio_file = st.file_uploader(
            "Upload/record a voice question",
            type=["mp3", "wav", "m4a"]
        )

    user_input = st.chat_input("Ask Macdini...")

    # If no text but audio used → transcribe
    if not user_input and audio_file:
        with st.spinner("Transcribing audio..."):
            try:
                user_input = transcribe_audio(audio_file)
                st.info(f"Transcribed: **{user_input}**")
            except Exception as e:
                st.error(f"Transcription failed: {e}")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Macdini is thinking..."):
                answer = call_macdini(st.session_state.chat_history)
                st.markdown(answer)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})


# ---------- MODE 2: CSV ANALYSIS ----------
elif mode == "CSV analysis":
    st.subheader("📊 CSV Upload & Analysis")

    uploaded = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            st.session_state.df = df

            st.markdown("#### Data Preview")
            st.dataframe(df.head())

            st.markdown("#### Summary Statistics")
            st.dataframe(df.describe(include="all", datetime_is_numeric=True))

            question = st.text_input(
                "Ask a question about this dataset:",
                placeholder="Example: Which column affects sales the most?"
            )

            if st.button("Analyze"):
                sample = df.head(10).to_csv(index=False)
                summary = df.describe(include="all", datetime_is_numeric=True).to_string()

                extra = (
                    "You are analyzing a CSV dataset for the user.\n"
                    f"Sample rows (first 10):\n{sample}\n\n"
                    f"Summary statistics:\n{summary}\n\n"
                    f"User question: {question}"
                )

                with st.spinner("Analyzing dataset..."):
                    answer = call_macdini([], extra_instructions=extra)
                    st.markdown("#### Macdini's Analysis")
                    st.markdown(answer)

        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    else:
        st.info("Upload a CSV to start.")


# ---------- MODE 3: PRACTICE QUIZ ----------
elif mode == "Practice quiz":
    st.subheader("📝 Practice Quiz")

    topic = st.selectbox(
        "Choose topic",
        [
            "Python basics", "Pandas", "SQL fundamentals",
            "Joins & GROUP BY", "Statistics", "Probability",
            "Regression vs classification", "Model evaluation"
        ]
    )

    difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
    num_q = st.slider("Number of questions", 3, 15, 5)

    if st.button("Generate Quiz"):
        instructions = (
            "Generate a quiz with only the questions, no answers.\n"
            f"Topic: {topic}\n"
            f"Difficulty: {difficulty}\n"
            f"Number of questions: {num_q}"
        )

        with st.spinner("Creating quiz..."):
            quiz = call_macdini([], extra_instructions=instructions)
            st.markdown("#### Your Quiz")
            st.markdown(quiz)
