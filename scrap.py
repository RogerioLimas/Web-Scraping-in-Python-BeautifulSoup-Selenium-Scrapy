import pathlib
import sys
import time
from bs4 import BeautifulSoup
import requests


def safe_file_name(filename):
    invalid_chars = '\/:*?"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


root = "https://subslikescript.com"

website = f'{root}/movies_letter-A'
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')

# Pagination
pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')
last_page = pages[-2].text

links = []

for page in range(1, int(last_page) + 1)[:2]:
    print(f"Processing page {page}/{last_page}...\n", end='\r')
    result = requests.get(f'{website}?page={page}')
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    box = soup.find('article', class_='main-article')

    for link in box.find_all('a', href=True):
        links.append(link['href'])

    i = 1

    for link in links:
        try:
            print(f"Processing {link} - {i}/{len(links)}...", end='\r')

            result = requests.get(f'{root}/{link}')
            content = result.text
            soup = BeautifulSoup(content, 'lxml')

            box = soup.find('article', class_='main-article')

            title = box.find('h1').getText()
            transcript = box.find(
                'div', class_='full-script').get_text(strip=True, separator=' ')

            filename = f'scripts\\{safe_file_name(title)}.txt'.replace(
                '/', '_')

            with open(filename, 'w', encoding='utf-8') as file:
                file.write(transcript)
                file.flush()

            i += 1

        except Exception as e:
            print("------ Link not working ------")
            print(e)
            print(f"Error processing {link} - {i}/{len(links)}...", end='\r')
