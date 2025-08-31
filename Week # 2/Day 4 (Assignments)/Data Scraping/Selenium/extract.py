from bs4 import BeautifulSoup
import pandas as pd
import os

news_data = []

for file in os.listdir("data"):
    if file.endswith(".html"):
        try:
            with open(f"data/{file}", "r", encoding="utf-8") as f:
                html_doc = f.read()
                
            soup = BeautifulSoup(html_doc, "html.parser")
            
            title_tag = soup.select_one("h2")
            title = title_tag.get_text(strip=True) if title_tag else "N/A"
            
            link_tag = soup.select_one("a")
            link = link_tag.get("href") if link_tag else "N/A"
            
            date_tag = soup.select_one("span.date")
            date = date_tag.get_text(strip=True) if date_tag else "N/A"
            
            description = title

            news_data.append({
                "title": title,
                "link": link,
                "description": description,
                "date": date
            })
            
        except Exception as e:
            print(f"Error processing file {file}: {e}")

df = pd.DataFrame(data=news_data)
df.to_csv("news.csv", index=False)
print(f"Successfully extracted {len(news_data)} news articles and saved to news.csv")