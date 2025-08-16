from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Navigate to the app
            page.goto("http://localhost:8080", timeout=60000)

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

            # Wait for the first download link to be visible
            first_download_link = page.get_by_role("link", name="Download").first
            expect(first_download_link).to_be_visible(timeout=10000)

            # Start waiting for the download
            with page.expect_download() as download_info:
                first_download_link.click()

            download = download_info.value

            # Wait for the download to complete
            path = download.path()

            # Check that the downloaded file is not empty
            import os
            assert os.path.getsize(path) > 0

            # Check if the filename is correct
            suggested_filename = download.suggested_filename
            print(f"Suggested filename: {suggested_filename}")
            assert "Rick Astley" in suggested_filename
            assert "dQw4w9WgXcQ" in suggested_filename

            print("Download verification successful.")

            # Take a screenshot
            page.screenshot(path="jules-scratch/verification/verification.png")
            print("Screenshot saved to jules-scratch/verification/verification.png")

        except Exception as e:
            print(f"An error occurred during verification: {e}")
            # Try to capture a screenshot even on failure for debugging
            page.screenshot(path="jules-scratch/verification/error.png")
            print("Error screenshot saved to jules-scratch/verification/error.png")

        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()
