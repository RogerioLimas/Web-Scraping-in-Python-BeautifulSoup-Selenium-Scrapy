import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


website = 'https://www.adamchoi.co.uk/overs/detailed'

options = Options()
# options.add_argument('--headless')
options.add_argument("--window-size=100,500")
options.log.level = "error"

driver = webdriver.Firefox(options=options, service_log_path='NUL')
driver.get(website)

path = "//label[text()='All matches']"

all_matches_button = driver.find_element(By.XPATH, path)
all_matches_button.click()

dropdown = Select(driver.find_element(By.ID, 'country'))
dropdown.select_by_visible_text('Brazil')

matches = driver.find_elements(By.TAG_NAME, 'tr')

date = []
home_team = []
score = []
away_team = []

i = 1

for match in matches:
    tds = match.find_elements(By.TAG_NAME, 'td')
    date.append(tds[0].text)
    home_team.append(tds[1].text)
    score.append(tds[2].text)
    away_team.append(tds[3].text)

    i += 1
    print(f'{i}/{len(matches)}', end='\r')

    # print(f'{tds[0].text} {tds[1].text} {tds[2].text} {tds[3].text}', end='\r')

df = pd.DataFrame({'Date': date, 'Home Team': home_team,
                  'Score': score, 'Away Team': away_team})

df.to_csv('matches.csv', index=False)

# input('Hit something...')
# driver.quit()
