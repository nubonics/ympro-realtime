import httpx
from .models import Task


class ExternalApiClient:
    def __init__(self, client: httpx.AsyncClient, base_url: str):
        self.client = client
        self.base_url = base_url

    async def fetch_workbasket(self):
        resp = await self.client.get(f"{self.base_url}/workbasket")
        resp.raise_for_status()
        return [Task(**t) for t in resp.json()["tasks"]]

    async def fetch_hostlers_summary(self):
        resp = await self.client.get(f"{self.base_url}/hostlers/summary")
        resp.raise_for_status()
        return resp.json()["hostlers"]

    async def fetch_hostler_details(self, hostler_id: str):
        resp = await self.client.get(f"{self.base_url}/hostlers/{hostler_id}/details")
        resp.raise_for_status()
        return [Task(**t) for t in resp.json().get("tasks", [])]

    async def fetch_task_details(self, task_id: str):
        resp = await self.client.get(f"{self.base_url}/tasks/{task_id}")
        resp.raise_for_status()
        return resp.json()["task"]

    async def patch_task(self, task_id: str, patch_data: dict):
        resp = await self.client.patch(f"{self.base_url}/tasks/{task_id}", json=patch_data)
        resp.raise_for_status()
        return resp.json()["task"]

    async def delete_task(self, task_id: str):
        resp = await self.client.delete(f"{self.base_url}/tasks/{task_id}")
        return resp.status_code in (200, 204, 404)
