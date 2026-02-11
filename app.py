import streamlit as st
import google.generativeai as genai

# 1. Page Config
st.set_page_config(page_title="Research Persona", layout="wide")
st.title("🔍 Custom Research Assistant")

# 2. Get API Key safely from Secrets
# We will set this key up in the final step on Streamlit
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 3. Define the Persona & Internet Tool
# Edit the 'instruction' below if you want to change the persona
instruction = "You are a professional researcher. Use Google Search for every query to find the latest info. Always cite your links."

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=instruction,
    tools=[{"google_search_retrieval": {}}]
)

# 4. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("What are we researching?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # This sends the prompt to Gemini with Search enabled
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
