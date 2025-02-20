from flask import Flask, request, jsonify
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_ollama import ChatOllama
from tools.general_tools import set_alarm
from flask_apscheduler import APScheduler

app = Flask(__name__)

scheduler = APScheduler()

def configure_scheduler(app):
    scheduler.init_app(app)

    @scheduler.task('cron', id='helloworld', minute=3)
    def helloworld():
        with app.app_context():
            print("Hello World")

    scheduler.start()

configure_scheduler(app)

def load_tools():
    tools_list = {
        "set_alarm":set_alarm
    }
    return tools_list

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    tools_list = load_tools()

    llm = ChatOllama(model="llama3.2:latest")
    llm_with_tools = llm.bind_tools(list(tools_list.values()))

    messages = [HumanMessage(prompt)]
    ai_response = llm_with_tools.invoke(messages)
    messages.append(ai_response)

    if not ai_response.tool_calls:
        return jsonify({"response": ai_response.content})

    for tool_call in ai_response.tool_calls:
        tool_name = tool_call["name"].lower()
        selected_tool = tools_list.get(tool_name)
        if selected_tool:
            tool_response = selected_tool.invoke(tool_call["args"])
            messages.append(ToolMessage(tool_response, tool_call_id=tool_call["id"]))

    final_response = llm_with_tools.invoke(messages)

    return jsonify({"response": final_response.content})

if __name__ == "__main__":
    app.run(debug=True)
