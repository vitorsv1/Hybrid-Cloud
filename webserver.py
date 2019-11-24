from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os 
import json

app = FastAPI()

ip = os.getenv('webserverIP')
address = 'http://' + ip +':8000'

class Tarefa(BaseModel):
    title: str
    description: str

#GET
@app.get("/tarefa")
async def get_tarefa():
    a = requests.get(url = address + '/tarefa')
    return a.json()

@app.get("/tarefa/{id}")
async def get_tarefa_id(id: str):
    a = requests.get(url = address + '/tarefa/' + id )
    return a.json()

@app.get("/healthcheck", status_code=200)
async def health_check():
    a = requests.get(url = address + '/healthcheck')
    return a.json()

#POST
@app.post("/tarefa")
async def post_tarefa(tarefa: tarefa):
    data = {
        "title": tarefa.title, 
        "description": tarefa.description}
    requests.post(url = address + '/tarefa', data = json.dumps(data))

#PUT
@app.put("/tarefa/{id}")
async def put_tarefa_id(id: str, tarefa: tarefa):
    data = {
        "title": tarefa.title, 
        "description": tarefa.description}
    a = requests.put(url = address + '/tarefa/' + id, data = json.dumps(data) )

#DELETE
@app.delete("/tarefa/{id}")
async def delete_tarefa(id: str):
    a = requests.delete(url = address + '/tarefa/' + id )
