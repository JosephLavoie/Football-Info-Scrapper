import time
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the WebDriver (for example, using Chrome)
driver = webdriver.Chrome()

url = "https://www.pro-football-reference.com/boxscores/200009030mia.htm"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table with the id "kicking"
    kicking_table = soup.find('table', {'id': 'kicking'})

    # Extract and print the headers
    headers = [header.text.strip() for header in kicking_table.select('thead th')]
    print(headers)

    # Extract and print only FGM and FGA
    for row in kicking_table.select('tbody tr'):
        player_info = [info.text.strip() for info in row.select('th, td')]
        player_name = player_info[0]
        fgm = player_info[headers.index('FGM')]
        fga = player_info[headers.index('FGA')]
        print("Player:", player_name)
        print("FGM:", fgm)
        print("FGA:", fga)
        print("----------")
        
    print("happened")

else:
    print("error")
print("done")