import asyncio
import os
from urllib.parse import urlparse
import pandas as pd
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator, PruningContentFilter

urls_to_crawl = ["https://www.daraz.pk/catalog/?spm=a2a0e.tm80335142.search.d_go&q=Laptop", "https://www.amazon.com/s?k=laptop&crid=2RFTPA1V9N14W&sprefix=lapt%2Caps%2C443", "https://www.ebay.com/sch/i.html?_nkw=laptop&_sacat=0&_from=R40&_ipg=240"]

async def main():
    browser_conf = BrowserConfig(headless=True)  
    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS
    )
    async with AsyncWebCrawler(config=browser_conf) as crawler:
        results = await crawler.arun_many(
            urls=urls_to_crawl,
            config=CrawlerRunConfig(stream=False, 
                                    markdown_generator=DefaultMarkdownGenerator(
                                        content_filter=PruningContentFilter()
                                        ),
                                    ) 
        )

        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)

        for i, res in enumerate(results, start=1):
            if res.success:
                parsed = urlparse(res.url)
                print(parsed)
                domain = parsed.netloc.replace(":", "_")
                filename = f"{i}_{domain}.html"
                filepath = os.path.join(output_dir, filename)
                try:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(res.fit_html or "")
                    print(f"Saved: {filepath}")
                except Exception as e:
                    print(f"Failed to save {res.url}: {e}")
            else:
                print("Failed:", res.url, "-", res.error_message)

if __name__ == "__main__":
    asyncio.run(main())