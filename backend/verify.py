import asyncio
import os
from playwright.async_api import async_playwright
import httpx

ARTIFACT_DIR = r"C:\Users\hichi\.gemini\antigravity\brain\9b9b7421-903a-49e8-b205-ebba8aa285d6"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})

        # 1. Landing Page
        await page.goto("http://localhost:5173")
        await page.wait_for_selector("text=Skincare")
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "landing.png"))
        print("Took screenshot of landing page.")

        # 2. Skincare Flow -> Dry Skin
        await page.click("text=Skincare")
        await page.wait_for_selector("text=Next") # Wait for quiz to load
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "quiz_question.png"))
        print("Took screenshot of quiz question.")

        # Answer 5 questions favoring Dry Skin (usually Option A)
        for i in range(5):
            # Select first radio or button, assuming it maps to A
            buttons = await page.locator("button:not(:has-text('Next')):not(:has-text('Back')):not(:has-text('See'))").all()
            if buttons:
                await buttons[0].click()
            
            next_btn = page.locator("button:has-text('Next')")
            submit_btn = page.locator("button:has-text('See Results')")
            if await next_btn.is_visible():
                await next_btn.click()
            elif await submit_btn.is_visible():
                await submit_btn.click()
                
            await page.wait_for_timeout(500)

        # Wait for results to load
        await page.wait_for_selector("text=Retake Quiz")
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "skincare_results.png"))
        print("Took screenshot of skincare results.")

        # 3. Haircare Flow -> Oily Scalp, High Porosity
        await page.click("text=Retake Quiz")
        await page.wait_for_selector("text=Haircare")
        await page.click("text=Haircare")
        await page.wait_for_selector("text=Next")

        # Scalp quiz (3 questions) - Oily is B
        for i in range(3):
            buttons = await page.locator("button:not(:has-text('Next')):not(:has-text('Back')):not(:has-text('See'))").all()
            if len(buttons) > 1:
                await buttons[1].click() # Option B
            
            next_btn = page.locator("button:has-text('Next')")
            submit_btn = page.locator("button:has-text('See Results')")
            if await next_btn.is_visible():
                await next_btn.click()
            elif await submit_btn.is_visible():
                await submit_btn.click()
            
            await page.wait_for_timeout(500)

        # Porosity quiz (4 questions) - High is C
        for i in range(4):
            buttons = await page.locator("button:not(:has-text('Next')):not(:has-text('Back')):not(:has-text('See'))").all()
            if len(buttons) > 2:
                await buttons[2].click() # Option C
            elif buttons:
                 await buttons[-1].click()
            
            # The last question might have a "See Results" or "Submit" instead of Next
            next_btn = page.locator("button:has-text('Next')")
            submit_btn = page.locator("button:has-text('See Results')")
            if await next_btn.is_visible():
                await next_btn.click()
            elif await submit_btn.is_visible():
                await submit_btn.click()
            
            await page.wait_for_timeout(500)

        # Wait for results
        await page.wait_for_selector("text=Retake Quiz")
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "haircare_results.png"))
        print("Took screenshot of haircare results.")

        await browser.close()
        
    # Check health API
    resp = httpx.get("http://localhost:8000/api/health")
    print("Health check status:", resp.status_code)
    assert resp.status_code == 200

if __name__ == "__main__":
    asyncio.run(main())
