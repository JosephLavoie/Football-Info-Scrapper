import time
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the WebDriver (for example, using Chrome)
driver = webdriver.Chrome()


def Information_Getter(game_url_list):
    infoCSV = []
    bad_infoCSV = []
    line = 0

    for url in game_url_list:

        time.sleep(5)
        response = requests.get(url)

        wait_time = response.headers.get('Retry-After')

        if wait_time:
            print(wait_time)
            time.sleep(int(wait_time) + 1)
            response = requests.get(url)
        
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            #---------------------------------------------------------------------------------------
            # Statium
            #---------------------------------------------------------------------------------------

            statium_element = soup.find('a', href=lambda href: href and href.startswith("/stadiums/"))

            if statium_element:
                statium = statium_element.text
            else:
                print("Missing: Statium")
                statium = "N/A"

            #---------------------------------------------------------------------------------------
            # Roof
            #---------------------------------------------------------------------------------------
            
            #---------------------------------------------------------------------------------------
            # Surface
            #---------------------------------------------------------------------------------------

            #---------------------------------------------------------------------------------------
            # Field Goals
            #---------------------------------------------------------------------------------------

            #---------------------------------------------------------------------------------------
            # Weather
            #---------------------------------------------------------------------------------------
            
            
            infoCSV.append(statium + "," + roof + "," + surface + "," + fga + "," + fgm + "," + weather)
        else:
            print(f"Failed to retrieve the HTML content. Status code: {response.status_code}")
            bad_infoCSV.append(url + "," + str(line))


        print(f"#{line} out of ~8000")
        line += 1


    return [infoCSV, bad_infoCSV]


def main():
    print("Use 'bad_infoCSV.txt' instead of game_url_list.txt?")
    user_input = input("Y/N: ")

    gameUrls = []

    if user_input == "N":
        with open('game_url_list.txt', 'r') as file:
            # Read each line from the file and append it to the list
            for line in file:
                gameUrls.append(line.strip())
        
    else:
        with open('bad_infoCSV.txt', 'r') as file:
            # Read each line from the file and append it to the list
            for line in file:
                gameUrls.append(line.strip())

    infoLine = Information_Getter(gameUrls)

    with open('infoCSV.txt', 'a') as file:
        # Convert each element of the list to a string and write it to the file
        for item in infoLine[0]:
            file.write(str(item) + '\n')
    
    with open('bad_infoCSV.txt', 'w') as file:
        # Convert each element of the list to a string and write it to the file
        for item in infoLine[1]:
            file.write(str(item) + '\n')

if __name__ == "__main__":
    main()
