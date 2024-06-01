from starlette.config import Config
from starlette.datastructures import Secret
 
try:
    config = Config(".env")
except FileNotFoundError: 
    config = Config()   
 
DATABASE_URL:str = config("DATABASE_URL", cast=Secret)

BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER", cast=str)
KAFKA_TODO_TOPIC = config("KAFKA_TODO_TOPIC", cast=str)
KAFKA_CONSUMER_GROUP_ID_FOR_TODO = config("KAFKA_CONSUMER_GROUP_ID_FOR_TODO", cast=str)
Gemini_API_KEY = config("Gemini_API_KEY" , cast=str)