from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Navigate to the app
            page.goto("http://localhost:8080", timeout=60000)

            # Wait for the main container to be visible
            container = page.locator(".container")
            expect(container).to_be_visible(timeout=10000)

            # Input a YouTube URL
            youtube_url_input = page.get_by_placeholder("Enter YouTube URL")
            expect(youtube_url_input).to_be_visible(timeout=10000)
            youtube_url_input.fill("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

            # Click the button to get video info
            get_info_btn = page.get_by_role("button", name="Get Video Info")
            get_info_btn.click()

            # Wait for the title to appear to ensure the info has loaded
            video_title = page.locator("#video-title")
            expect(video_title).to_contain_text("Rick Astley", timeout=30000)

            # Take a screenshot
            page.screenshot(path="jules-scratch/verification/verification.png")
            print("Screenshot saved to jules-scratch/verification/verification.png")

        except Exception as e:
            print(f"An error occurred during verification: {e}")
            page.screenshot(path="jules-scratch/verification/error.png")
            print("Error screenshot saved to jules-scratch/verification/error.png")

        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()
