from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from typing import Optional, Annotated
from sqlmodel import Field, SQLModel, create_engine, Session, select
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio 

from todo import settings 
from suggestions import send_suggestion

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
    asyncio.create_task(consume_messages('nextasproducer', 'broker:19092'))
    yield


# FastAPI Instance
app = FastAPI(lifespan=lifespan, title="FASTAPI WITH DB",version="1.0.0")

def get_session():
    with Session(engine) as session:
        yield session 

# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

# # # Adding TODO TO DATABASE
@app.post("/api/todos/", response_model=TodoHomework)
async def create_todo(todo: TodoHomework, session: Annotated[Session, Depends(get_session)] , producer:Annotated[AIOKafkaProducer, Depends(get_session)]):
    
    # Sending AI SUGGESSTIONS to the kafka topics
    prodMessage = await producer.send_and_wait("aisuggestions", b"Super message")
    print("prodMessage",prodMessage)
    
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