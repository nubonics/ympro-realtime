# Real-time Task Board Backend (FastAPI + Redis + Pydantic v2)

## Features

- Strict task models (Pydantic v2, discriminated unions)
- Redis backend for task persistence
- Real-time updates: Redis Pub/Sub and FastAPI WebSocket endpoint
- CORS enabled
- Easy to extend

## Quickstart

1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
2. Start Redis server:
    ```
    redis-server
    ```
3. Run the backend:
    ```
    uvicorn api:app --reload
    ```
4. Endpoints:
    - `GET /api/external-tasks` — List all tasks
    - `POST /api/create-task` — Create a task (JSON body)
    - `POST /api/update-task-hostler` — Update a task's hostler
    - `POST /api/delete-task` — Delete a task
    - `WS /ws/tasks` — WebSocket for real-time events

5. Frontend: Connect to the WebSocket for real-time updates.

## Notes

- All task fields stored as strings in Redis.
- All real-time events are triggered only by backend API actions.