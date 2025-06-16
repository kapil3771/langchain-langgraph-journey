import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import gradio as gr
from day08_branching_agent.graph import get_agent_graph, memory

graph = get_agent_graph()

def chat_fn(message, chat_history):
    result = graph.invoke({"input": message})
    response = result["response"]

    chat_history = chat_history + [{"role": "user", "content": message}, {"role": "assistant", "content": response}]

    try:
        memory_preview = memory.search(message, k=3)
        memory_text = "\n".join([f"🔹 {doc.page_content}" for doc in memory_preview])
    except Exception as e:
        memory_text = f"Could not fetch memory: {str(e)}"

    return chat_history, chat_history, memory_text


# 🍸 Cyberpunk Modern Theme
modern_css = """
body {
    background: #12151c;
    font-family: 'Segoe UI', Roboto, sans-serif;
    color: #e0e0e0;
}

.gradio-container {
    max-width: 900px;
    margin: auto;
    padding-top: 30px;
}

.gr-chatbot {
    border: 1px solid #2d2f3a;
    border-radius: 12px;
    background: rgba(30, 33, 43, 0.6);
    backdrop-filter: blur(10px);
}

.gr-textbox textarea {
    background: #1c1e26 !important;
    color: #00ffc8 !important;
    border: 1px solid #2f3340 !important;
    border-radius: 10px;
    font-size: 16px;
}

.gr-textbox textarea::placeholder {
    color: #666;
}

button {
    background: linear-gradient(90deg, #00ffc8, #0077ff);
    color: black;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    transition: 0.2s ease-in-out;
}

button:hover {
    transform: scale(1.03);
    opacity: 0.9;
}

.gr-textbox label {
    font-weight: bold;
    color: #9efff5;
}

.gr-box {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid #292d3e;
    border-radius: 10px;
    padding: 12px;
    margin-top: 12px;
}
"""

with gr.Blocks(css=modern_css, theme=gr.themes.Base()) as demo:
    gr.Markdown("## 🤖 Branching Agent <span style='color:#00ffc8;'>with Memory</span>", elem_id="title")

    chatbot = gr.Chatbot(label="", height=400, type="messages")
    state = gr.State([])

    with gr.Row():
        msg = gr.Textbox(
            label="💬 Type your message",
            placeholder="Say hi or ask the current time...",
            scale=5,
        )

    memory_box = gr.Textbox(
        label="🧠 FAISS Memory Results",
        lines=5,
        interactive=False,
    )

    with gr.Row():
        submit = gr.Button("Send 🚀")

    submit.click(chat_fn, [msg, state], [chatbot, state, memory_box])
    msg.submit(chat_fn, [msg, state], [chatbot, state, memory_box])

demo.launch()