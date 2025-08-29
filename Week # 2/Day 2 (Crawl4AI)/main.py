import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator, PruningContentFilter
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

query = "laptop"
file = 0
# os.makedirs("data", exist_ok=True)

async def main():
    browser_conf = BrowserConfig(headless=False)  # or False to see the browser
    run_conf = CrawlerRunConfig(
        css_selector=".su-card-container",
        cache_mode=CacheMode.BYPASS,
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=PruningContentFilter()
            )
        )

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        for i in range(1,2):
            result = await crawler.arun(
                url=f"https://www.ebay.com/sch/i.html?_nkw={query}&_sacat=0&_from=R40&_ipg=240&_pgn={i}", 
                config=run_conf
            )
            # print(result.markdown)
            print(f"Page {i}: Found {len(result)} elements")
            print(type(result))
            output_path = "ebay.html"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result.fit_html)
            print(f"Markdown saved to: {output_path}")

if __name__ == "__main__":
    asyncio.run(main())

