from flask import Flask, render_template, jsonify
import speech_recognition as sr
import threading

app = Flask(__name__)

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
            # Speech not understood
            continue
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            break

def hotword_trigger_action():
    print("Hotword action triggered!")

@app.route('/')
def home():
    return render_template('index.html')

def start_hotword_detection():
    thread = threading.Thread(target=hotword_detection)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    start_hotword_detection()
    app.run(host='0.0.0.0', port=5000)
