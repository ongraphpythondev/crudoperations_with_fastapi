from fastapi import FastAPI,Depends,status, HTTPException
from database import Base, engine,get_db
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models

class ToDoRequest(BaseModel):
    task: str

Base.metadata.create_all(engine)

app = FastAPI()

@app.post("/create_todo_list/")
def details_input(request:ToDoRequest,db: Session = Depends(get_db)):
    new_task = models.ToDo(task=request.task)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "List created successfully", "status": "success"}

@app.get("/todo_list/")
def read_todo(db:Session = Depends(get_db)):
    task = db.query(models.ToDo).all()
    print(task)
    return {"todo list": task, "status": "success"}


@app.get("/todo/{id}")
def read_todo(id,db:Session = Depends(get_db)):
    task = db.query(models.ToDo).filter(models.ToDo.id==id).first()
    if task:
        return {"todo item": task, "status": "success"}
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/todo/{id}")
def delete_todo(id,db:Session=Depends(get_db)):
    delete_task=db.query(models.ToDo).filter(models.ToDo.id==id).delete()
    if delete_task:
        db.commit()
        return {"message": f"Deleted successfully with id {id}", "status": "success"} 
    raise HTTPException(status_code=404, detail=f"Item with id {id} not found")


@app.put("/update_todo/{id}")
def updated_todo(id,request:ToDoRequest,db:Session=Depends(get_db)):
    updated_task=db.query(models.ToDo).filter(models.ToDo.id==id)
    print(updated_task)
    if updated_task:
        updated_task.update(request.model_dump())
        db.commit()
        return {"message": f"Updated list with id {id}", "status": "success"}
    raise HTTPException(status_code=404, detail=f"Item with id {id} not found")



