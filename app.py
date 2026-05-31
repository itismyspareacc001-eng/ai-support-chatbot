
# ==========================================================
# AI SUPPORT CHATBOT
# Day 15 Project
#
# Technologies:
# - Python
# - Streamlit
# - Gemini API
#
# Features:
# - AI Chat
# - Chat History
# - Sidebar
# - Clear Chat
# - Message Statistics
# - Download Chat
# ==========================================================

# ==========================================================
# IMPORT LIBRARIES
# ==========================================================

import streamlit as st
import google.generativeai as genai


# ==========================================================
# GEMINI CONFIGURATION
# ==========================================================

GEMINI_API_KEY = "AIzaSyD6XMlVUe3YtUDhrhFx_nkRcOBDP_PFGcg"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


# ==========================================================
# PAGE SETTINGS
# ==========================================================

st.set_page_config(
    page_title="AI Support Chatbot",
    page_icon="🤖",
    layout="wide"
)
st.caption(
    "Chatbot with Conversation Memory"
)


# ==========================================================
# SESSION STATE
# Stores all chat messages
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("⚙️ Chatbot Settings")

    st.markdown("---")

    st.success("Model: Gemini 2.5 Flash")

    st.markdown("---")

    st.info(
        """
        ### AI Support Chatbot

        Built Using:
        - Python
        - Streamlit
        - Gemini API

        Features:
        - Chat Interface
        - Memory
        - Export Chat
        - Statistics
        """
    )

    st.markdown("---")

    # ======================================================
    # MESSAGE STATISTICS
    # ======================================================

    total_messages = len(
        st.session_state.messages
    )

    user_messages = sum(
        1
        for msg in st.session_state.messages
        if msg["role"] == "user"
    )

    ai_messages = sum(
        1
        for msg in st.session_state.messages
        if msg["role"] == "assistant"
    )

    st.metric(
        "Total Messages",
        total_messages
    )

    st.metric(
        "User Messages",
        user_messages
    )

    st.metric(
        "AI Responses",
        ai_messages
    )

    st.markdown("---")

    # ======================================================
    # CLEAR CHAT BUTTON
    # ======================================================

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# ==========================================================
# MAIN TITLE
# ==========================================================

st.title("🤖 AI Support Chatbot")

st.markdown(
    "Ask anything and get intelligent responses from Gemini AI."
)

st.markdown("---")


# ==========================================================
# DISPLAY OLD CHAT HISTORY
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# ==========================================================
# USER INPUT
# ==========================================================

user_prompt = st.chat_input(
    "Type your message..."
)


# ==========================================================
# PROCESS USER MESSAGE
# ==========================================================

if user_prompt:

    # ------------------------------------------------------
    # SHOW USER MESSAGE
    # ------------------------------------------------------

    st.chat_message("user").markdown(
        user_prompt
    )

    # Save User Message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # ------------------------------------------------------
    # CALL GEMINI
    # ------------------------------------------------------

    try:

        # ============================================
        # BUILD CONVERSATION HISTORY
        # ============================================

        conversation = ""

        for msg in st.session_state.messages:

            role = msg["role"]

            content = msg["content"]

            conversation += f"{role}: {content}\n"


        conversation += f"user: {user_prompt}"


# ============================================
# SEND FULL CONTEXT TO GEMINI
# ============================================

        response = model.generate_content(
            conversation
        )

        ai_response = response.text

    except Exception as e:

        ai_response = (
            f"Error: {str(e)}"
        )

    # ------------------------------------------------------
    # SHOW AI RESPONSE
    # ------------------------------------------------------

    with st.chat_message("assistant"):

        st.markdown(
            ai_response
        )

    # Save AI Message

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_response
        }
    )


# ==========================================================
# DOWNLOAD CHAT SECTION
# ==========================================================

st.markdown("---")

st.subheader("📥 Export Conversation")

chat_history = ""

for msg in st.session_state.messages:

    role = msg["role"].upper()

    content = msg["content"]

    chat_history += (
        f"{role}:\n"
        f"{content}\n\n"
    )

st.download_button(
    label="Download Chat History",
    data=chat_history,
    file_name="chat_history.txt",
    mime="text/plain"
)