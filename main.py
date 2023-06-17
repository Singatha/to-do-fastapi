from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import sqlite3

app = FastAPI()


class Task(BaseModel):
    task_name: str
    task_description: str
    task_status: str


@app.on_event("startup")
async def startup():
    # Create a connection to the SQLite database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Create a table (if not exists) for todos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            task_description VARCHAR(255),
            task_status VARCHAR(255),
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

@app.get("/api/tasks")
async def get_tasks():
    # Connect to the SQLite database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Retrieve all todos from the table
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    # Close the connection
    conn.close()

    return {"tasks": tasks}

@app.post("/api/tasks/create")
async def create_tasks(task: Task):
    # Connect to the SQLite database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Insert the new todo into the table
    cursor.execute("INSERT INTO tasks (task_name, task_description, task_status) VALUES (?, ?, ?)", (task.task_name, task.task_description, task.task_status))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return {"message": "Task created successfully"}

@app.put("/api/tasks/update/{task_id}")
async def update_task(task_id: int, task: Task):
    # Connect to the SQLite database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Update the completed status of the todo
    cursor.execute("UPDATE tasks SET task_name = ?, task_description = ?, task_status = ? WHERE task_id = ?", (task.task_name, task.task_description, task.task_status, task_id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return {"message": "Task updated successfully"}

@app.delete("/api/tasks/delete/{task_id}")
async def delete_task(task_id: int):
    # Connect to the SQLite database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Delete the todo from the table
    cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return {"message": "Tasks deleted successfully"}
