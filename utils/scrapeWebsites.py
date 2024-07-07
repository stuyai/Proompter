import asyncio
from playwright.async_api import async_playwright


async def scrape_p_text(url:str) -> str:
    '''
    Scrapes all the text from the <p> tags on a webpage
    
    This usually only works for the websites BBC, the Verge, or AP News (which are the only websites I have tested this on)
    '''
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        
        # Get all text from <p> tags
        p_tags = await page.query_selector_all('p')
        p_texts = [await p.text_content() for p in p_tags]
        
        await browser.close()
        
        text = " ".join(p_texts)
        text.replace("  ", " ")
        return text
