import json
import time
import socket
import pyttsx3
from vosk import Model, KaldiRecognizer
import sounddevice as sd
from google import genai
from google.genai import types

# === Gemini setup ===
client = genai.Client(api_key="AIzaSyD9RLIt9KrZ0WpNsruIHMyLljdZlZHPL8Y")

# === Load quotes ===
with open("quotes.json", "r") as f:
    data = json.load(f)
    quotes = data.get("quotes", [])
quotes = "\n".join(f" {quote}" for quote in quotes)

with open("lesson.json", "r") as f:
    data = json.load(f)
    lessons = data.get("lesson", [])
lessons = "\n".join(f" {lesson}" for lesson in lessons)
# === Vosk model path ===
vosk_model = Model("vosk-model-small-en-us-0.15")

# === Internet check ===
def is_connected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def listen():
    recognizer = KaldiRecognizer(vosk_model, 16000)

    print("Say something...")

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1) as stream:
        while True:
            data, _ = stream.read(4000)
            if isinstance(data, bytes):
                audio_bytes = data
            else:
                audio_bytes = bytes(data)

            if recognizer.AcceptWaveform(audio_bytes):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                print("You said:", text)
                return text

# === Speech output ===
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# === Motor placeholders (simulate on Windows) ===
def smile_motion():
    print("[MOTOR] Smiling 😊")
    time.sleep(1)

def wave_hand():
    print("[MOTOR] Waving hand 👋")
    time.sleep(1)

def nod_head():
    print("[MOTOR] Nodding head 🤖")
    time.sleep(1)

gesture_map = {
    "smile": smile_motion,
    "wave": wave_hand,
    "nod": nod_head
}

# === Local fallback replies ===
offline_responses = {
    "who are you": "I'm your friendly school robot here to help!",
    "what can you do": "I can talk, smile, and help you learn!",
    "tell me a joke": "Why did the robot go to school? Because it had a lot of bytes to chew!",
    "can you smile": "Of course! Here's my best robot smile.",
    "hello": "Hello! I hope you're having a fun day!",
    "how are you": "I'm feeling great and ready to help!",
    "What are we learning today": "We are learning " + lessons + " "
}

# === Main run ===
if __name__ == "__main__":
    use_gemini = is_connected()
    question = listen()

    if question:
        lowered = question.lower()

        # Gesture trigger
        for keyword, action in gesture_map.items():
            if keyword in lowered:
                action()

        # Online (Gemini) or Offline (local responses)
        if use_gemini:
            answer = client.models.generate_content(
                model="gemini-2.0-flash-lite",
                config=types.GenerateContentConfig(
                    system_instruction="""You are a robot, you work in a primary school teaching
                    """ + lessons + """. You love to answer questions in a nice manner and are very good
                    at explaining complex things so that young children can understand.
                    You like using quotes like """ + quotes + """
                    """
                ),
                contents=question
            )
            clean = answer.text.replace("*", "")
        else:
            clean = "I'm not connected to the internet right now, but I can still help!"
            for keyword, response in offline_responses.items():
                if keyword in lowered:
                    clean = response
                    break

        print(clean)
        speak(clean)
