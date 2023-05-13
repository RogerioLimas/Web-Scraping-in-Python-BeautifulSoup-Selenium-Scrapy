from attr import dataclass
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


options = Options()
options.add_argument('--headless')

driver = webdriver.Firefox(options=options)

web = 'https://www.audible.com/search'

driver.get(web)

container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container')
products = container.find_elements(
    By.XPATH, './/li[contains(@class, "productListItem")]')

@dataclass
class Product:
    title: str
    author: str
    length: str


titles = []
authors = []
lengths = []

for product in products:
    title = product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text
    author = product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]/span/a').text
    length = product.find_element(
        By.XPATH, './/li[contains(@class, "runtimeLabel")]/span').text.replace('Length: ', '')
    
    titles.append(title)
    authors.append(author)
    lengths.append(length)

driver.quit()


df = pd.DataFrame({'Title': titles, 'Author': authors, 'Length': lengths})
df.to_csv('products.csv', index=False)
