from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson.objectid import ObjectId
import sys
import pymongo
import os 

ip = os.getenv("mongoIP")
addr = "mongodb://" + ip + ":27017/"
#addr = "mongodb://localhost:27017"


myclient = pymongo.MongoClient(addr) 
mydb = myclient["mongoDatabase"]
tarefasdb = mydb["tarefas"]

app = FastAPI()

class Task(BaseModel):
    title: str
    description: str

@app.get("/tarefa")
async def get_tarefa():
    res = {}
    res["Data"] = []
    for i in tarefasdb.find():
        res["Data"].append(
            {'id': str(i["_id"]), 
             'title': i["title"], 
             'description': i["description"]})
    return res

@app.get("/healthcheck", status_code=200)
async def health_check():
    return

@app.get("/tarefa/{id}")
async def get_tarefa_id(id: str):
    res = {}
    res["Data"] = []
    for i in tarefasdb.find( {"_id": ObjectId(id)} ):
        res["Data"].append(
            {'id': str(i["_id"]),
             'title': i["title"],
             'description': i["description"]})
    return res

@app.post("/tarefa")
async def post_tarefa(tarefa: Task):
    dictio = {"title": tarefa.title, "description": tarefa.description}
    tarefasdb.insert_one(dictio)

@app.put("/tarefa/{id}")
async def put_tarefa_id(id: str, tarefa: Task):
    tarefasdb.update_one(
        {"_id": ObjectId(id)}, 
        {"$set": 
            {"title": tarefa.title, 
             "description": tarefa.description}})
    
@app.delete("/tarefa/{id}")
async def delete_tarefa(id: str):
    tarefasdb.remove( {"_id": ObjectId(id)} )
