from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from typing import Optional, Annotated
from todo import settings  
from sqlmodel import Field, SQLModel, create_engine, Session, select

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
        
@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Creating Tables")
    create_db_and_tables()
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