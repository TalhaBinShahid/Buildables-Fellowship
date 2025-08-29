from bs4 import BeautifulSoup
import pandas as pd

import os

d=[]

for file in os.listdir("data"):
    try:
        with open(f"data/{file}", "r", encoding="utf-8") as f:
            html_doc = f.read()
            
        soup = BeautifulSoup(html_doc, "html.parser")
        title_tag = soup.select_one(".RfADt a")
        title = title_tag.get("title") if title_tag else "N/A"

        link_tag = soup.select_one(".RfADt a")
        link = link_tag.get("href") if link_tag else "N/A"

        price_tag = soup.select_one(".ooOxS")
        price = price_tag.get_text() if price_tag else "N/A"

        d.append({
            "title": title,
            "price": price,
            "link": link
        })
    except Exception as e:
        print(f"Error processing file {file}: {e}")

df = pd.DataFrame(data=d)
df.to_csv("daraz_products.csv")


