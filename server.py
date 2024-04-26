from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any

app = FastAPI()

# Sample weather data
weather_data = {
    "japan": {
        "tokyo": "Sunny",
    },
    "canada": {
        "ottawa": "Rainy",
    },
    "usa": {
        "washington_dc": "Cloudy",
    },
    "china": {
        "beijing": "Snowy",
    },
}

# Sample todo data
todo_data: dict[str, Any] = {}


class Task(BaseModel):
    task: str


@app.get("/weather")
def get_weather(region: str, town: str, date: str):
    # date は割愛。文字列日付の為、本来は PARSE して使用する。
    print("access", region, town, date)

    try:
        return {"result": weather_data[region][town]}
    except:
        return {"result": "could not be get"}


@app.get("/todo/{username}")
def get_todo_list(username: str):
    print(f"access: POST:/todo/{username}")
    if username in todo_data:
        return todo_data[username]
    else:
        return []


@app.post("/todo/{username}")
def add_task(username: str, task: Task):
    print(f"access: POST:/todo/{username}", task)
    try:
        if username in todo_data:
            todo_data[username].append(task.task)
        else:
            todo_data[username] = [task.task]
        return {"result": "Task added successfully"}
    except:
        return {"result": "Task add failed"}
