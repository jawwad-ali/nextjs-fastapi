from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from typing import Optional, Annotated
from todo import settings
from sqlmodel import Field, SQLModel, create_engine, Session, select
from aiokafka import AIOKafkaConsumer
import asyncio 
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


# Making Todo table with data validation 
class TodoHomework(SQLModel , table=True): 
    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str] = Field(index=True) 
    isCompleted: Optional[bool] = Field(default=False , index=True)
    
connection_string = str(settings.DATABASE_URL).replace(  
    "postgresql", "postgresql+psycopg" 
)   
 
# recycle connections after 5 minutes 
# to correspond with the compute scale down  
engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)

# DB instance and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
        
async def send_suggestion(word:str):
    print("Crazy stuff dude.. "+ word )
    response = chat_session.send_message("give a 2 one word suggesstions related to " + word)

    print("Gemini Response =>> ",response.text)

# Kafka Consumer Function
async def consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-todos-group",
        auto_offset_reset='earliest' 
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(message)
            print(f"Received message: {message.value.decode()} on topic {message.topic}")
            await send_suggestion(message.value.decode())
            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally: 
        # Ensure to close the consumer when done.
        await consumer.stop()



@asynccontextmanager
async def lifespan(app:FastAPI):
    task = asyncio.create_task(consume_messages('nextasproducer', 'broker:19092'))
    yield


# FastAPI Instance
app = FastAPI(lifespan=lifespan, title="FASTAPI WITH DB",version="1.0.0")

def get_session():
    with Session(engine) as session:
        yield session 


# # # Adding TODO TO DATABASE
@app.post("/api/todos/", response_model=TodoHomework)
def create_todo(todo: TodoHomework, session: Annotated[Session, Depends(get_session)]):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
 
# # Fetching Todos
@app.get("/api/todos", response_model=list[TodoHomework])
def read_todos(session: Annotated[Session, Depends(get_session)]):
        todos = session.exec(select(TodoHomework)).all()
        return todos 
 
# # Delete Todos-
@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):

    statement = select(TodoHomework).where(TodoHomework.id == todo_id)
    results = session.exec(statement)
    todo = results.one()
    
    session.delete(todo)  
    session.commit()

    return {"message": f"{todo.title} deleted successfully"}


# With Kakfa