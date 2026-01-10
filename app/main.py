import streamlit as st
from agent import get_agent

st.set_page_config(page_title="PotatoGPT", layout="wide")
st.title("🥔 PotatoGPT (Ollama + LangChain)")

if "messages" not in st.session_state:
    st.session_state.messages = []

agent = get_agent() # This is where the AI pipeline is built.

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Ask something...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = agent.invoke(prompt)
        st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
