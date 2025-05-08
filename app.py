from dotenv import load_dotenv
from speechtotext import SpeechRecognizer
from texttospeech import TextToSpeech
from llm import LLMCompanion

load_dotenv()

if __name__ == "__main__":
    
    stt=SpeechRecognizer() #speech to text
    tts=TextToSpeech()   #text to speech
    llm=LLMCompanion()

    tts.speak("Welcome back , how can i help you?")
    # try:
    while True:
        input = stt.listen()       #stt.listen()
        print("You:", input)
        if input.lower() in ["exit", "quit", "stop"]:
            tts.speak("Goodbye!")
            break
        
        intent=llm.detect_intent(input)
        print(intent)
        
        #data
        data={
            "objects":{
                "bottle":"left"
            },
            "scene":"kitchen",
            "intent":intent,
            "input":input
        }

        response = llm.generate_response(data, input)
        print(f"AI: {response}")
        tts.speak(response)

    # except KeyboardInterrupt:
    #     print("\nExiting on user request.")
    # except Exception as e:
    #     print(f" Unexpected error: {e}")
