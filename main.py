import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from services.get_models_list import get_ollama_models_list
from services.get_title import get_chat_title
from services.chat_utilities import get_answer
from db.conversations import (
    create_new_conversation,
    add_message,
    get_conversation,
    get_all_conversations,
)

st.set_page_config(page_title="Privy AI", page_icon="💬", layout="centered")
st.title("🤖 Local ChatGPT Clone")

# ---- Models ----
# session state is used to store selected model across interactions
if "OLLAMA_MODELS" not in st.session_state:
    st.session_state.OLLAMA_MODELS = get_ollama_models_list()

selected_model = st.selectbox("Select Model", st.session_state.OLLAMA_MODELS)

# ---- Session state ----
# here we initialize session state variables to manage conversation context
st.session_state.setdefault("conversation_id", None)
st.session_state.setdefault("conversation_title", None)
st.session_state.setdefault("chat_history", [])  # [{role, content}]

# ---- Sidebar: conversations ----
with st.sidebar:
    st.header("💬 Chat History")
    conversations = get_all_conversations()  # {conv_id: title}

    if st.button("➕ New Chat"):
        st.session_state.conversation_id = None
        st.session_state.conversation_title = None
        st.session_state.chat_history = []

    # List existing conversations
    # highlight current conversation
    # clicking a conversation loads its history
    # iterate over conversations dict
    # this code creates buttons for each conversation in the sidebar and loads the selected conversation's history
    for cid, title in conversations.items():
        is_current = cid == st.session_state.conversation_id
        label = f"**{title}**" if is_current else title
        if st.button(label, key=f"conv_{cid}"):
            doc = get_conversation(cid) or {}
            st.session_state.conversation_id = cid
            st.session_state.conversation_title = doc.get("title", "Untitled")
            st.session_state.chat_history = [
                {"role": m["role"], "content": m["content"]} for m in doc.get("messages", [])
            ]

# ---- Show chat so far ----
# iterate over chat history and display messages
# seesion_state.chat_history is a list of dicts with role and content
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# here we handle user input and generate assistant responses and persist them
# ---- Chat input ----
user_query = st.chat_input("Ask AI...")
if user_query:
    # 1) Show + store user message in UI state
    st.chat_message("user").markdown(user_query)
    st.session_state.chat_history.append({"role": "user", "content": user_query})

    # 2) Persist to DB (create convo on first message, else append)
    if st.session_state.conversation_id is None:
        try:
            title = get_chat_title(selected_model, user_query) or "New Chat"
        except Exception:
            title = "New Chat"
        conv_id = create_new_conversation(title=title, role="user", content=user_query)
        st.session_state.conversation_id = conv_id
        st.session_state.conversation_title = title
    else:
        add_message(st.session_state.conversation_id, "user", user_query)

    # 3) Get assistant response (direct service)
    try:
        assistant_text = get_answer(selected_model, st.session_state.chat_history)
    except Exception as e:
        assistant_text = f"[Error getting response: {e}]"

    # 4) Show + store assistant message
    with st.chat_message("assistant"):
        st.markdown(assistant_text)
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_text})

    # 5) Persist assistant message
    if st.session_state.conversation_id:
        add_message(st.session_state.conversation_id, "assistant", assistant_text)