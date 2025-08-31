import json
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai import JsonCssExtractionStrategy


genre = "Philosophy"
lang = "English"
async def extract_books_data():
    schema = {
        "name": "Books Data",
        "baseSelector": "div.su-card-container--horizontal",    # Repeated elements
        "fields": [
            {
                "name": "book_photo",
                "selector": "img.s-card__image",
                "type": "attribute",
                "attribute": "src"
            },
            {
                "name": "book_name",
                "selector": "div.s-card__title",
                "type": "text"
            },
            {
                "name": "price",
                "selector": "span.s-card__price",
                "type": "text"
            },
            {
                "name": "book_rating",
                "selector": "div.x-star-rating",
                "type": "text"
            },
            {
                "name":"book_description",
                "selector": "div.s-card__subtitle-row",
                "type": "text"
            }
        ]
    }

    # 2. Create the extraction strategy
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
    config = CrawlerRunConfig(
        cache_mode = CacheMode.BYPASS,
        extraction_strategy=extraction_strategy,
    )
    
    all_books_data = []  # Store all books from all pages
    total_pages = 10
    
    async with AsyncWebCrawler(verbose=True) as crawler:
        for page in range(1, total_pages + 1):
            print(f"\n--- Scraping Page {page}/{total_pages} ---")
            
            # Calculate the starting item number for each page
            # eBay uses _pgn parameter for pagination (page number)
            start_item = (page - 1) * 240 + 1
            
            # 4. Run the crawl and extraction for current page
            result = await crawler.arun(
                url=f"https://www.ebay.com/sch/i.html?_dcat=261186&_fsrp=1&rt=nc&_from=R40&_nkw=books&_sacat=0&Genre={genre}&Language={lang}&_ipg=240&_pgn={page}",
                config=config
            )

            if not result.success:
                print(f"Page {page} crawl failed:", result.error_message)
                continue

            # 5. Parse the extracted JSON
            page_data = json.loads(result.extracted_content)
            
            # Add page number to each book entry for tracking
            for book in page_data:
                book["page_number"] = page
            
            all_books_data.extend(page_data)
            print(f"Page {page}: Extracted {len(page_data)} books. Total so far: {len(all_books_data)}")
            
            # Optional: Add a small delay between requests to be respectful
            await asyncio.sleep(1)
        
        print(f"\n=== FINAL RESULTS ===")
        print(f"Total books extracted from {total_pages} pages: {len(all_books_data)}")
        
        if all_books_data:
            print("Sample book data:")
            print(json.dumps(all_books_data[0], indent=2))
        
        # Save all data to JSON file
        with open("books_data.json", "w", encoding="utf-8") as f:
            json.dump(all_books_data, f, ensure_ascii=False, indent=4)
        
        print(f"\nAll data saved to books_data.json")

asyncio.run(extract_books_data())