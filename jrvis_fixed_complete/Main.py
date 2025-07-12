import eel
import os
import subprocess
import pyttsx3
import speech_recognition as sr

eel.init("web")

# Initialize voice engine
engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("voice", engine.getProperty('voices')[1].id)

def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()

# App list - update with your installed apps
software_map = {
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "photoshop": "C:\\Program Files\\Adobe\\Adobe Photoshop 2024\\Photoshop.exe"
}

@eel.expose
def handle_command(command):
    command = command.lower().strip()

    if "open" in command:
        for name, path in software_map.items():
            if name in command:
                try:
                    subprocess.Popen(path)
                    speak(f"Opening {name}")
                    return f"✅ Opening {name}"
                except Exception as e:
                    speak(f"Failed to open {name}")
                    return f"❌ Failed to open {name}: {e}"
        speak("Software not found.")
        return "⚠️ Software not recognized."

    elif "close" in command:
        for name, path in software_map.items():
            if name in command:
                os.system(f"taskkill /f /im {os.path.basename(path)}")
                speak(f"Closing {name}")
                return f"🛑 Closed {name}"
        speak("Software to close not found.")
        return "⚠️ Software not recognized to close."

    elif command in ["hi", "hello", "jarvis"]:
        speak("Hello Siddhant. I am online and ready.")
        return "Hello Siddhant. I am online and ready."

    speak(f"You said: {command}")
    return f"You said: {command}"

@eel.expose
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio)
            return handle_command(query)
        except sr.UnknownValueError:
            speak("Sorry, I did not understand.")
            return "❌ I couldn't understand you."
        except Exception as e:
            speak("Microphone error.")
            return f"❌ Mic error: {e}"

# Launch app
eel.start("index.html", size=(800, 600), port=8088)
