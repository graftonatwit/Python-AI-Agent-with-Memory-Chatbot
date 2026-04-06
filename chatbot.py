from openai import OpenAI
import os

# 🔑 Set your API key here or use environment variable
client = OpenAI()

# 🧠 Conversation memory
messages = [
    {"role": "system", "content": "You are a helpful AI assistant. You can chat and use tools like a calculator when needed."}
]

# 🧮 Tool: Calculator
def calculate(expression):
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return "Error in calculation."

# 🛠️ Tool handler
def use_tool(user_input):
    if user_input.startswith("calc "):
        expression = user_input.replace("calc ", "")
        return calculate(expression)
    return None

# 🤖 AI Agent loop
def run_agent():
    print("🤖 AI Agent started! Type 'exit' to quit.")
    print("💡 Use 'calc 2+2' for calculations.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Agent: Goodbye!")
            break

        # 🔧 Check if tool should be used
        tool_result = use_tool(user_input)
        if tool_result:
            print("Agent:", tool_result)
            continue

        # 🧠 Add user message to memory
        messages.append({"role": "user", "content": user_input})

        try:
            # 💬 Get AI response
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )

            reply = response.choices[0].message.content

            # 🧠 Save AI response
            messages.append({"role": "assistant", "content": reply})

            print("Agent:", reply)

        except Exception as e:
            print("Error:", e)

# ▶️ Run the agent
if __name__ == "__main__":
    run_agent()