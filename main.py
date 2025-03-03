# from fastapi import FastAPI,HTTPException
# import uvicorn
# from pydantic import BaseModel
# from  typing import List, Optional
# from uuid import UUID,uuid4
# app = FastAPI()

# class Task( BaseModel): #defining fields
#     id:Optional[UUID]=None 
#     title:str
#     description:Optional[str]=None
#     completed:bool=False 

# tasks=[]

# @app.post("/tasks/",response_model=Task)
# def create_task(task:Task):
#     task.id=uuid4()
#     tasks.append(task)
#     return task

# @app.get("/tasks/",response_model=List[Task])
# def read_tasks():
#     return tasks

# @app.get("/tasks/{task_id}",response_model=Task)
# def read_task(task_id:UUID):
#     for task in tasks:
#         if task.id==task_id:
#             return task
#     raise HTTPException(status_code=404,detail="Task not found")

# @app.put("/tasks/{task_id}",response_model=Task)
# def update_task(task_id:UUID,task_update:Task):
#     for idx,task in enumerate(tasks):
#         if task.id==task_id:
#             updated_task=task.copy(update=task_update.dict(exclude_unset=True))
#             tasks[idx]=updated_task
#             return updated_task
#     raise HTTPException(status_code=404,detail="task not found") 

# @app.delete("/tasks/{task_id}",response_model=Task)
# def delete_task(task_id):
#     for idx,task in enumerate(tasks):
#         if task.id==task_id:
#             return tasks.pop(idx)
#     raise HTTPException(status_code=404,detail="task not found") 

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8080)
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI()

class Task( BaseModel): #defining fields
    id:Optional[UUID]=None 
    title:str
    description:Optional[str]=None
    completed:bool=False 

tasks: List[Task] = []

@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    task.id=uuid4()
    tasks.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)  # Fixed route
def read_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_update: Task):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = task.model_copy(update=task_update.model_dump(exclude_unset=True))  # Fixed for Pydantic v2
            tasks[idx] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: UUID):  # Fixed type annotation
    for idx, task in enumerate(tasks):
        if task.id == task_id:  # Fixed variable name
            return tasks.pop(idx)
    raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
