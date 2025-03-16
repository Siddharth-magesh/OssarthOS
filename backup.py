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