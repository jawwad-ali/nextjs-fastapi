import os
import google.generativeai as genai

genai.configure(api_key=os.environ["Gemini_API_KEY"])
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64, 
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain", 
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(history=[])

async def send_suggestion(word:str):
    print("Crazy stuff dude.. "+ word )
    response = chat_session.send_message("give a 2 one word suggesstions related to " + word)

    print("Gemini Response =>> ",response.text)