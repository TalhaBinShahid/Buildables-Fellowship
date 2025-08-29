from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
query="laptop"
for i in range(1, 5):
    driver.get(f"https://www.daraz.pk/catalog/?page={i}&q={query}")
    elems = driver.find_elements(By.CLASS_NAME, "Bm3ON")
    print(f"Found {len(elems)} elements")

    for elem in elems:
        print(elem.text)

# print(elem.get_attribute("outerHTML"))

driver.close()