import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse, parse_qs, unquote

def extract_httpx_snippet(request):
    parsed = urlparse(request.url)
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    params = {k: v[0] for k, v in parse_qs(parsed.query).items()}
    headers = dict(request.headers)
    method = request.method
    post_data = request.post_data or ""

    # Build httpx snippet
    code = f"# Recreated from Playwright\n"
    code += f"import httpx\n\n"
    code += f"async def send():\n"
    code += f"    async with httpx.AsyncClient() as client:\n"
    code += f"        response = await client.request(\n"
    code += f"            method='{method}',\n"
    code += f"            url='{base_url}',\n"
    if params:
        code += f"            params={params},\n"
    if method == "POST" and post_data:
        code += f"            data={repr(post_data)},\n"
    code += f"            headers={headers}\n"
    code += f"        )\n"
    code += f"        print(response.status_code)\n"
    code += f"        print(response.text[:500])\n"
    return code


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        page.on("request", lambda request: print(extract_httpx_snippet(request)))

        print(">> Log in manually and open a case. Watching network requests...")
        await page.goto("https://ymg.estes-express.com/prweb/app/YardMgmt/")

        await page.wait_for_timeout(120_000)  # 2 minutes to complete the flow manually

        await browser.close()

asyncio.run(main())
