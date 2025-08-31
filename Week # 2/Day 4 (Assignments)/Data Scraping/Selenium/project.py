from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

driver = webdriver.Chrome()

os.makedirs("data", exist_ok=True)
driver.get("https://www.geo.tv/category/pakistan")
time.sleep(3)
title = driver.title
print(title)

# driver.implicitly_wait(0.5)

i = 1
elems = driver.find_elements(By.CLASS_NAME, "entry-title")
d = elems[0].get_attribute("outerHTML")
with open(f"data/news_{i}.html", "w", encoding="utf-8") as f:
    f.write(d)

elems = driver.find_elements(By.CLASS_NAME, "border-box")
for elem in elems:
    d = elem.get_attribute("outerHTML")
    with open(f"data/news_{i}.html", "w", encoding="utf-8") as f:
        f.write(d)
    i += 1  
    # time.sleep(2)

driver.quit()
