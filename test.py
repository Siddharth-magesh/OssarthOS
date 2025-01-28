from flask import Flask, request, jsonify, render_template
import requests
import threading
import speech_recognition as sr

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def call_ollama_model(prompt):
    payload = {
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return None

def set_alarm(time):
    return f"Alarm set for {time}"

def set_reminder(task, date):
    return f"Reminder set for {task} on {date}"

def check_weather(location):
    return f"Weather in {location}: Sunny, 25°C"

@app.route('/function-call', methods=['POST'])
def function_call():
    data = request.json
    prompt = data.get("prompt")
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    response = call_ollama_model(prompt)
    
    if not response:
        return jsonify({"error": "Failed to call Ollama model"}), 500
    
    if "set alarm" in response.lower():
        time = extract_time_from_prompt(prompt)
        if not time:
            return jsonify({"error": "No time specified for alarm"}), 400
        result = set_alarm(time)
    elif "set reminder" in response.lower() or "set task" in response.lower():
        task, date = extract_task_and_date_from_prompt(prompt)
        if not task or not date:
            return jsonify({"error": "No task or date specified for reminder"}), 400
        result = set_reminder(task, date)
    elif "check weather" in response.lower():
        location = extract_location_from_prompt(prompt)
        if not location:
            return jsonify({"error": "No location specified for weather check"}), 400
        result = check_weather(location)
    else:
        return jsonify({"error": "No valid function detected in the prompt"}), 400
    
    return jsonify({"result": result})

def extract_time_from_prompt(prompt):
    if "at" in prompt:
        return prompt.split("at")[1].strip()
    return None

def extract_task_and_date_from_prompt(prompt):
    if "on" in prompt:
        parts = prompt.split("on")
        task = parts[0].replace("set reminder", "").replace("set task", "").strip()
        date = parts[1].strip()
        return task, date
    return None, None

def extract_location_from_prompt(prompt):
    if "in" in prompt:
        return prompt.split("in")[1].strip()
    return None

def hotword_detection(hotword="mark"):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    print("Listening for the hot word...")

    while True:
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            
            detected_text = recognizer.recognize_google(audio)
            print(f"You said: {detected_text}")
            
            if hotword.lower() in detected_text.lower():
                print(f"Hotword '{hotword}' detected!")
                hotword_trigger_action()
        except sr.UnknownValueError:
            continue
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            break

def hotword_trigger_action():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    print("Hotword action triggered! Listening for a command...")
    
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        
        command = recognizer.recognize_google(audio)
        print(f"Voice command: {command}")
        
        response = call_ollama_model(command)
        if response:
            print(f"Ollama response: {response}")
        else:
            print("Failed to process the command.")
    except sr.UnknownValueError:
        print("Could not understand the command.")
    except sr.RequestError as e:
        print(f"Error with voice recognition: {e}")

@app.route('/')
def home():
    return render_template('index.html')

def start_hotword_detection():
    thread = threading.Thread(target=hotword_detection)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    start_hotword_detection()
    app.run(debug=True, host='0.0.0.0', port=5005)
