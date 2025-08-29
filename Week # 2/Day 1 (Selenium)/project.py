from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

driver = webdriver.Chrome()
query = "laptop"
file = 0
os.makedirs("data", exist_ok=True)

for i in range(1, 20):
    driver.get(f"https://www.daraz.pk/catalog/?page={i}&q={query}")
    elems = driver.find_elements(By.CLASS_NAME, "Bm3ON")
    print(f"Page {i}: Found {len(elems)} elements")

    for elem in elems:
        d = elem.get_attribute("outerHTML")
        with open(f"data/{query}_{file}.html", "w", encoding="utf-8") as f:
            f.write(d)
        file += 1  
    time.sleep(2)

driver.close()