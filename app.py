import os
import importlib.util
import inspect
import re
import json
from utils.scheduler import check_alarms
from flask import Flask, request, jsonify , render_template
from flask_apscheduler import APScheduler
from werkzeug.utils import secure_filename
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_ollama import ChatOllama
from langchain_core.tools import StructuredTool

TOOLS_DIR = "./tools"
ALARM_FILE = "alarms.json"

app = Flask(__name__)
scheduler = APScheduler()
os.makedirs(TOOLS_DIR, exist_ok=True)

def configure_scheduler():
    scheduler.init_app(app)

    @scheduler.task('interval', id='check_alarms', minutes=1)
    def scheduled_alarm_checker():
        with app.app_context():
            check_alarms()

    scheduler.start()

configure_scheduler()

def load_tools():
    tools_list = {}

    for filename in os.listdir(TOOLS_DIR):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module_path = os.path.join(TOOLS_DIR, filename)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for name, func in inspect.getmembers(module):
                if isinstance(func, StructuredTool) or (callable(func) and hasattr(func, "_lc_tool")):
                    tools_list[name] = func

    return tools_list

@app.route("/askweb", methods=["POST"])
def askweb():
    prompt = request.form.get("prompt")

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
    return render_template("index.html", response=final_response.content)

@app.route("/ask", methods=["POST"])
def ask():
    prompt = request.form.get("prompt")

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
    return str(final_response.content)

@app.route("/add_tools", methods=["POST"])
def add_tools():
    if "files" not in request.files:
        return jsonify({"error": "No files provided"}), 400

    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No files uploaded"}), 400

    uploaded_files = []
    for file in files:
        filename = secure_filename(file.filename)
        if filename.endswith(".py"):
            file.save(os.path.join(TOOLS_DIR, filename))
            uploaded_files.append(filename)

    load_tools()

    return jsonify({"success": True, "files": uploaded_files, "message": "Tools added successfully!"}), 200

@app.route("/list_tools", methods=["GET"])
def list_tools():
    tools = list(load_tools().keys())
    return jsonify({"available_tools": tools})

@app.route("/remove_tool", methods=["DELETE"])
def remove_tool():
    data = request.json
    tool_name = data.get("tool_name")

    tool_path = os.path.join(TOOLS_DIR, f"{tool_name}.py")
    if os.path.exists(tool_path):
        os.remove(tool_path)
        return jsonify({"message": f"Tool '{tool_name}' removed successfully!"})

    return jsonify({"error": "Tool not found"}), 404

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3333, debug=True)
