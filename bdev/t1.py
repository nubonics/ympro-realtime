from playwright.sync_api import sync_playwright


def run_playwright_and_log_requests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Log all network requests
        def log_request(request):
            print(f"REQUEST: {request.method} {request.url}")
            if request.method == "POST":
                post_data = request.post_data or ''
                print(f"POST DATA: {post_data}")

        page.on("request", log_request)

        # Navigate to the yard management portal login
        page.goto("https://ymg.estes-express.com/prweb/app/YardMgmt")

        # Wait for manual login (user interaction)
        print(
            "👉 Please log in manually, then navigate to a case (e.g., T-34384995). Logging will happen automatically.")
        page.wait_for_timeout(120000)  # wait 2 minutes for user to interact

        browser.close()


run_playwright_and_log_requests()
