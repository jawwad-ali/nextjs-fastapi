from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from typing import Optional, Annotated
from todo import settings  
from sqlmodel import Field, SQLModel, create_engine, Session, select


# Making Todo table with data validation 
class TodoHomework(SQLModel , table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str] = Field(index=True)
    
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


@app.get("/api/todos") 
def read_root():
    return {"Hello": "Hello World from Poetry!!"}

def get_session():
    with Session(engine) as session:
        yield session
        
# # Adding TODO TO DATABASE
@app.post("/todos/", response_model=TodoHomework)
def create_todo(todo: TodoHomework, session: Annotated[Session, Depends(get_session)]):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
 
# # Fetching Todos
@app.get("/todos/", response_model=list[TodoHomework])
def read_todos(session: Annotated[Session, Depends(get_session)]):
        todos = session.exec(select(TodoHomework)).all()
        return todos 
 
# Delete Todos
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):

    statement = select(TodoHomework).where(TodoHomework.id == todo_id)
    results = session.exec(statement)
    todo = results.one()
    
    # print("todo: ", todo)

    session.delete(todo) 
    session.commit()

    return {"message": f"{todo.title} deleted successfully"}

# Update Todo
@app.patch("/todos/{todo_id}")
def update_hero(hero_id: int, hero: TodoHomework , session: Annotated[Session, Depends(get_session)]):
    db_hero = session.get(TodoHomework, hero_id)

    print("OLD db Hero",db_hero)
    
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data = hero.model_dump(exclude_unset=True)
    db_hero.sqlmodel_update(hero_data)

    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)

    print("updateTodo",db_hero)

    return db_hero