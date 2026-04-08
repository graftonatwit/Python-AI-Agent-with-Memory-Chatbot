from openai import OpenAI
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# ---------------------------
# Flask setup
# ---------------------------
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# ---------------------------
# OpenAI client
# ---------------------------
client = OpenAI()

# ---------------------------
# Conversation memory
# ---------------------------
messages = [
    {"role": "system", "content": "You are a helpful AI assistant. You can chat and use tools like a calculator when needed."}
]

# ---------------------------
# Calculator tool
# ---------------------------
def calculate(expression):
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception:
        return "Error in calculation."

def use_tool(user_input):
    stripped_input = user_input.lstrip().lower()
    if stripped_input.startswith("calc "):
        expression = stripped_input[5:].strip()
        return calculate(expression)
    return None

@app.route("/")
def index():
    return render_template("index.html")

# ---------------------------
# Flask API route
# ---------------------------
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    
    # Check if tool should be used
    tool_result = use_tool(user_input)
    if tool_result:
        return jsonify({"reply": tool_result})
    
    # Add user message
    messages.append({"role": "user", "content": user_input})
    
    # Get AI response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    
    return jsonify({"reply": reply})

@app.route("/reset", methods=["POST"])
def reset():
    global messages
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant. You can chat and use tools like a calculator when needed."}
    ]
    return jsonify({"status": "conversation reset"})

# ---------------------------
# CLI chatbot
# ---------------------------
def run_cli():
    print("🤖 AI Agent started! Type 'exit' to quit.")
    print("💡 Use 'calc 2+2' for calculations.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Agent: Goodbye!")
            break

        # Check if tool should be used
        tool_result = use_tool(user_input)
        if tool_result:
            print("Agent:", tool_result)
            continue

        messages.append({"role": "user", "content": user_input})
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            reply = response.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
            print("Agent:", reply)
        except Exception as e:
            print("Error:", e)

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    # Choose mode: CLI or Flask
    mode = input("Run in CLI or Web mode? (cli/web): ").strip().lower()

    if mode == "web":
        print("Starting Flask server on http://0.0.0.0:5000")
        app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    else:
        run_cli()