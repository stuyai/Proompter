import asyncio
from playwright.async_api import async_playwright


async def scrape_p_text(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        # Get all text from <p> tags
        p_tags = await page.query_selector_all("p")
        p_texts = [await p.text_content() for p in p_tags]

        await browser.close()

        return p_texts


async def main():
    url = "https://www.bbc.com/news/articles/cq5xjzqree2o"  # Replace with the URL you want to scrape
    p_texts = await scrape_p_text(url)
    print("Text in <p> tags:")
    text = " ".join(p_texts)
    text.replace("  ", " ")
    return text


if __name__ == "__main__":
    print(asyncio.run(main()))
    # scrape_p_text("https://www.bbc.com/news/articles/cq5xjzqree2o")
