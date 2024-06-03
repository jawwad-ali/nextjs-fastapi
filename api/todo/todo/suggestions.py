import os
import google.generativeai as genai
from aiokafka import AIOKafkaProducer
from fastapi import HTTPException

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

# Kafka Producer as a dependency
producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
async def get_kafka_producer():
    # FastAPI Producer function. events will be fired on "aisuggestions" topic  
    await producer.start()
    try:
        yield producer
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
    finally:
        await producer.stop()



async def send_suggestion(word:str):
    print("Crazy stuff dude.. "+ word )
    response = chat_session.send_message("give two a one-word suggesstions related to " + word)

    print("Gemini Response =>> ",  response.text)
    return response.text