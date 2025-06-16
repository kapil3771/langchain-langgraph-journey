import streamlit as st
from agent_graph import run_agent
from memory import MemoryManager

st.set_page_config(
    page_title="ReAct Agent 💬",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===== Style =====
st.markdown("""
    <style>
        body {
            background-color: #1E1E1E;
        }
        .stApp {
            background-color: #1E1E1E;
            color: #F0F0F0;
            font-family: 'Segoe UI', sans-serif;
        }
        .message {
            border-radius: 1rem;
            padding: 1rem;
            margin-bottom: 0.75rem;
        }
        .user-msg {
            background-color: #2A2A2A;
            align-self: flex-end;
        }
        .bot-msg {
            background-color: #333333;
            border-left: 4px solid #6C63FF;
        }
        .card {
            background-color: #2D2D2D;
            padding: 1rem;
            border-radius: 0.75rem;
            margin: 0.5rem 0;
            box-shadow: 0 0 10px rgba(0,0,0,0.25);
        }
    </style>
""", unsafe_allow_html=True)

# ===== Title =====
st.title("💬 Elegant ReAct Agent")

# ===== Memory Init =====
memory = MemoryManager()

# ===== Session State =====
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ===== Chat Input =====
user_input = st.chat_input("Ask something...")
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("Thinking..."):
        response, tools_used = run_agent(user_input, memory)
    st.session_state.chat_history.append(("agent", response))
    st.session_state.tools_used = tools_used

# ===== Chat Display =====
st.subheader("🧠 Conversation")
for role, msg in st.session_state.chat_history:
    css_class = "user-msg" if role == "user" else "bot-msg"
    st.markdown(f'<div class="message {css_class}">{msg}</div>', unsafe_allow_html=True)

# ===== Memory Preview =====
st.subheader("📚 Memory Preview")
docs = memory.retrieve_relevant(user_input or "test")
if docs:
    for doc in docs:
        st.markdown(f"<div class='card'>{doc.page_content}</div>", unsafe_allow_html=True)
else:
    st.markdown("No memory loaded yet.")

# ===== Tool Log Accordion =====
if "tools_used" in st.session_state and st.session_state.tools_used:
    st.subheader("🧰 Tools Used")
    with st.expander("Show Tool Logs"):
        for log in st.session_state.tools_used:
            st.markdown(f"<div class='card'>{log}</div>", unsafe_allow_html=True)