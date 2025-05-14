import requests
import json
import gradio as gr

# API setup
url = "http://localhost:11434/api/generate"
headers = {'Content-Type': 'application/json'}
history = []

# Generate response and maintain chat
def generate_response(prompt, chat_history):
    chat_history.append(("🧑 You", prompt))

    final_prompt = "\n".join([item[1] for item in chat_history if item[0] == "🧑 You"])

    data = {
        "model": "CodeWizard",
        "prompt": final_prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        data = json.loads(response.text)
        bot_response = data['response']
        chat_history.append(("🤖 CodeWizard", bot_response))
    else:
        bot_response = "❌ Error: " + response.text
        chat_history.append(("🤖 CodeWizard", bot_response))

    return "", chat_history

# Interface layout
with gr.Blocks(css="footer {display: none;}") as interface:
    gr.Markdown(
    """
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="
            font-size: 3em;
            font-weight: 900;
            background: linear-gradient(90deg, #00DBDE 0%, #FC00FF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
            margin-bottom: 10px;
        ">
            🤖 CodeWizard
        </h1>
        <p style="font-size: 1.1em; color: #CCCCCC;">
            Ask anything about code, AI, or your project – your intelligent assistant awaits.
        </p>
    </div>
    """
)

    chatbot = gr.Chatbot(label="Conversation with CodeWizard", height=400)
    input_box = gr.Textbox(
        lines=3,
        placeholder="Type your prompt here and press Enter or click 'Generate Response'...",
        label="💬 Your Prompt"
    )
    send_button = gr.Button("🚀 Generate Response")
    clear_button = gr.Button("🧹 Clear Chat")

    # Click or Enter to send
    input_box.submit(fn=generate_response, inputs=[input_box, chatbot], outputs=[input_box, chatbot])
    send_button.click(fn=generate_response, inputs=[input_box, chatbot], outputs=[input_box, chatbot])
    clear_button.click(lambda: ("", []), outputs=[input_box, chatbot])

interface.launch()
