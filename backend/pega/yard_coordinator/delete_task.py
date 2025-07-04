# delete_task.py
import asyncio
from datetime import datetime, timedelta
from os import getenv
from playwright.async_api import async_playwright, Page

LOGIN_URL = "https://ymg.estes-express.com/prweb/app/default"
SESSION_LIFETIME = timedelta(hours=11)


class DeleteTask:
    def __init__(self):
        self.task_set = set()
        self.task_cond = asyncio.Condition()
        self.browser = None
        self.context = None
        self.page: Page = None
        self.playwright = None
        self.last_login = None
        self.started = False

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        await self.login()
        self.started = True
        asyncio.create_task(self.worker())

    async def login(self):
        await self.page.goto(LOGIN_URL)
        await self.page.fill('input[name="UserIdentifier"]', getenv("PEGA_USERNAME"))
        await self.page.fill('input[name="Password"]', getenv("PEGA_PASSWORD"))
        await self.page.click('button[type="submit"]')
        await self.page.wait_for_selector('text=Dashboard', timeout=15000)
        self.last_login = datetime.utcnow()

    async def ensure_valid_session(self):
        if not self.last_login or (datetime.utcnow() - self.last_login > SESSION_LIFETIME):
            await self.login()

    async def run(self, case_id: str):
        async with self.task_cond:
            if case_id not in self.task_set:
                self.task_set.add(case_id)
                self.task_cond.notify()

    async def worker(self):
        while True:
            async with self.task_cond:
                while not self.task_set:
                    await self.task_cond.wait()
                case_id = self.task_set.pop()
            try:
                await self.ensure_valid_session()
                await self._delete(case_id)
            except Exception as e:
                print(f"[✖] Failed to delete {case_id}: {e}")

    async def _delete(self, case_id: str):
        if not self.page or self.page.is_closed():
            self.page = await self.context.new_page()
            await self.login()

        await self.page.locator('input[name="$PpyPortalHarness$ppySearchText"]').fill(case_id)
        await self.page.locator('i.pi.pi-search[title*="start search"]').click()

        delete_btn = self.page.locator('button:has-text("Delete")')
        await delete_btn.wait_for(state="visible", timeout=10000)
        await delete_btn.click()

        ok_btns = self.page.locator('button[name^="DeleteTask_pyWorkPage_"]')
        await ok_btns.first.wait_for(state="visible", timeout=10000)

        for i in range(await ok_btns.count()):
            btn = ok_btns.nth(i)
            if await btn.is_visible() and await btn.inner_text() == "OK":
                await btn.click()
                print(f"[✔] Deleted: {case_id}")
                return
        raise Exception("OK button not found")

    async def shutdown(self):
        if self.page: await self.page.close()
        if self.context: await self.context.close()
        if self.browser: await self.browser.close()
        if self.playwright: await self.playwright.stop()
