import os
import speech_recognition as sr
from openai import OpenAI
from gtts import gTTS
import pygame  
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv('API_KEY'),
    base_url="https://api.together.xyz/v1",
)

# Initialize pygame mixer
pygame.mixer.init()

def listen():
    """Capture voice input using microphone"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)
        return recognizer.recognize_google(audio)

def speak(text):
    """Convert text to speech using pygame"""
    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def chat_with_ai(prompt):
    """Get AI response from Together AI"""
    response = client.chat.completions.create(
        model="meta-llama/Llama-3-70b-chat-hf",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    try:
        while True:
            print("\n" + "="*40)
            user_input = listen()
            print(f"You: {user_input}")
            
            if user_input.lower() in ["exit", "quit", "stop"]:
                speak("Goodbye!")
                break
                
            response = chat_with_ai(user_input)
            print(f"AI: {response}")
            speak(response)
            
    except KeyboardInterrupt:
        speak("Goodbye!")
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, something went wrong")