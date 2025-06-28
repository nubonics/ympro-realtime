import os
import httpx
from typing import Any, Dict, Union

EXTERNAL_BASE_URL = os.getenv("EXTERNAL_TASK_API_URL", "http://localhost:9000/tasks")


async def create_task_external(task_data: Dict[str, Any]) -> httpx.Response:
    """
    Create a new task on the external API.
    Args:
        task_data: The task data to send (dict).
    Returns:
        httpx.Response: The response from the API.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(EXTERNAL_BASE_URL, json=task_data)
        return response


async def get_task_external(task_id: Union[str, int]) -> httpx.Response:
    """
    Retrieve a task from the external API by ID.
    Args:
        task_id: The ID of the task.
    Returns:
        httpx.Response: The response from the API.
    """
    url = f"{EXTERNAL_BASE_URL}/{task_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response


async def update_task_external(task_id: Union[str, int], update_data: Dict[str, Any]) -> httpx.Response:
    """
    Update an existing task on the external API.
    Args:
        task_id: The ID of the task to update.
        update_data: The fields to update (dict).
    Returns:
        httpx.Response: The response from the API.
    """
    url = f"{EXTERNAL_BASE_URL}/{task_id}"
    async with httpx.AsyncClient() as client:
        response = await client.put(url, json=update_data)
        return response


async def delete_task_external(task_id: Union[str, int]) -> httpx.Response:
    """
    Delete a task from the external API by ID.
    Args:
        task_id: The ID of the task.
    Returns:
        httpx.Response: The response from the API.
    """
    url = f"{EXTERNAL_BASE_URL}/{task_id}"
    async with httpx.AsyncClient() as client:
        response = await client.delete(url)
        return response
