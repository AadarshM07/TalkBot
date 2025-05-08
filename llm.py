import requests
import os
from openai import OpenAI

class LLMCompanion:
    
    def __init__(self):
        self.api_url = "https://api.together.xyz/v1/chat/completions"
        self.headers = {"Authorization": "Bearer tgp_v1_zb1v9W2rm3-yP40MdDer3tDE_U_LtNDtKpm3yPORsLc"}

        self.client = OpenAI(
            api_key=os.getenv('API_KEY'),
            base_url="https://api.together.xyz/v1",
        )
        

    def chat_with_ai(self, prompt):
        response = self.client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",
            messages=[{"role": "user", "content": prompt}]
        )

        response = response.choices[0].message.content
        return response

    def detect_intent(self, user_input):
        prompt = f"""
        Classify the user intent for the following message: '{user_input}'.
        Possible intents are: location, identify_objects, general_question.
        Respond with only the intent.

        Examples:

        Message: "Where am I?"
        Intent: location

        Message: "What can you see around me?"
        Intent: identify_objects

        Message: "How does this device work?"
        Intent: general_question

        Message: "Tell me what's to my left."
        Intent: identify_objects

        Message: "Am I in the living room?"
        Intent: location

        Message: "What's the weather like today?"
        Intent: general_question
        """
        
        return self.chat_with_ai(prompt)

    def generate_response(self, data, ques):
        scene = data.get("scene", None)
        objects = data.get("objects", {})
        intent = data.get("intent", "general_question")
        user_input=data.get("input")

        if intent == "location" or intent == "identify_objects":
                prompt = f"""
            You are an assistant helping a visually impaired person understand their surroundings.
            Based on the input scene and objects, respond clearly and naturally to their question.

            Input format:
            - "objects": dictionary of visible objects and their relative positions (e.g., left, right, front)
            - "scene": the name of the room or area

            Respond with a helpful and friendly message, describing the room and key objects around them.

            Example 1: 
            Question: Where am I?
            Input: {{
                "objects": {{
                    "chair": "right",
                    "table": "center"
                }},
                "scene": "dining_room"
            }}
            Output: You are in the dining room. There's a table in front of you and a chair to your right. Would you like help sitting down or moving elsewhere?

            Example 2: 
            Question: Find my phone?
            Input: {{
                "objects": {{
                    "laptop": "front",
                    "bookshelf": "left"
                }},
                "scene": "study_room"
            }}
            Output: You're in the study room. I see a laptop in front of you and a bookshelf to your left, but I don’t see a phone nearby.

            Example 3: 
            Question: Where am I?
            Input: {{
                "objects": {{
                    "remote": "left",
                    "tv": "center"
                }},
                "scene": "living_room"
            }}
            Output: You’re in the living room. There's a TV straight ahead and a remote to your left. Let me know if you want to turn it on or find something else.

            Input: '{data}'
            Question: {ques}
            """
        
        else:
            prompt = f"user said: '{user_input}'. As a polite and friendly voice assistant, respond naturally and appropriately. Your tone should be warm, helpful, and conversational—just like a human voice agent."

        ai_response = self.chat_with_ai(prompt)
        return ai_response


if __name__ == "__main__":
    llm=LLMCompanion()
    print(llm.detect_intent("find my bottle"))