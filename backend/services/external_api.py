import httpx

# Base URL for the external task API (update as needed)


async def create_task_external(task_data):
    """
    Create a new task on the external API.
    Args:
        task_data (dict): The task data to send.
    Returns:
        httpx.Response: The response from the API.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(EXTERNAL_BASE_URL, json=task_data)
        return response


async def get_task_external(task_id):
    """
    Retrieve a task from the external API by ID.
    Args:
        task_id (str|int): The ID of the task.
    Returns:
        httpx.Response: The response from the API.
    """
    url = f"{EXTERNAL_BASE_URL}/{task_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response


async def update_task_external(task_id, update_data):
    """
    Update an existing task on the external API.
    Args:
        task_id (str|int): The ID of the task to update.
        update_data (dict): The fields to update.
    Returns:
        httpx.Response: The response from the API.
    """
    url = f"{EXTERNAL_BASE_URL}/{task_id}"
    async with httpx.AsyncClient() as client:
        response = await client.put(url, json=update_data)
        return response


async def delete_task_external(task_id):
    """
    Delete a task from the external API by ID.
    Args:
        task_id (str|int): The ID of the task.
    Returns:
        httpx.Response: The response from the API.
    """
    url = f"{EXTERNAL_BASE_URL}/{task_id}"
    async with httpx.AsyncClient() as client:
        response = await client.delete(url)
        return response
