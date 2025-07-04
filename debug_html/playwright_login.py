import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

USERNAME = "222886"
PASSWORD = "123456"


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://ymg.estes-express.com/prweb/app/default")

        try:
            # Wait for username and password fields
            await page.locator('input[name="UserIdentifier"]').wait_for(timeout=10000)
            await page.locator('input[name="Password"]').wait_for(timeout=10000)

            # Fill credentials
            await page.fill('input[name="UserIdentifier"]', USERNAME)
            await page.fill('input[name="Password"]', PASSWORD)

            # Click the submit button
            await page.click('button[type="submit"]')

            print("Login submitted.")

        except PlaywrightTimeoutError:
            print("Login fields not found within timeout")

        await asyncio.sleep(1000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
